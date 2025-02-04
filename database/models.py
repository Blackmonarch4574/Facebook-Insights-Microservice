from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class SocialMediaUser(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str
    profile_pic: Optional[str] = None
    facebook_id: Optional[str] = None

class Post(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    page_id: str
    content: str
    likes_count: int
    comments_count: int
    shares_count: int
    posted_at: datetime
    media_urls: List[str] = []

class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    post_id: str
    user_id: str
    content: str
    likes_count: int
    commented_at: datetime

class FacebookPage(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    page_name: str
    username: str
    url: str
    facebook_id: str
    profile_pic: str
    email: Optional[str] = None
    website: Optional[str] = None
    category: str
    total_followers: int
    total_likes: int
    creation_date: datetime
    posts: List[Post] = []
    followers: List[SocialMediaUser] = []
    following: List[SocialMediaUser] = []
