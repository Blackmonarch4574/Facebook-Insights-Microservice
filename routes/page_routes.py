from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from services.scraper import FacebookPageScraper
from database.models import FacebookPage
from database.mongodb import Database

router = APIRouter()

@router.get("/page/{username}", response_model=FacebookPage)
async def get_page_details(
    username: str, 
    min_followers: Optional[int] = Query(None, ge=0),
    max_followers: Optional[int] = Query(None, ge=0)
):
    collection = Database.get_collection('facebook_pages')
    
    # Check if page exists in database
    existing_page = await collection.find_one({"username": username})
    
    if not existing_page:
        # Scrape page if not in database
        scraped_data = await FacebookPageScraper.scrape_page(username)
        
        if not scraped_data:
            raise HTTPException(status_code=404, detail="Page not found")
        
        # Insert scraped data into database
        result = await collection.insert_one(scraped_data)
        scraped_data['_id'] = result.inserted_id
        existing_page = scraped_data
    
    # Apply follower count filters
    if min_followers is not None and existing_page['total_followers'] < min_followers:
        raise HTTPException(status_code=404, detail="Page does not meet minimum follower criteria")
    
    if max_followers is not None and existing_page['total_followers'] > max_followers:
        raise HTTPException(status_code=404, detail="Page does not meet maximum follower criteria")
    
    return existing_page

@router.get("/pages", response_model=List[FacebookPage])
async def list_pages(
    name_search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    collection = Database.get_collection('facebook_pages')
    
    query = {}
    if name_search:
        query['page_name'] = {'$regex': name_search, '$options': 'i'}
    
    total_pages = await collection.count_documents(query)
    pages = await collection.find(query).skip((page-1)*page_size).limit(page_size).to_list(page_size)
    
    return pages
