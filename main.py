from fastapi import FastAPI
from database.mongodb import Database
from routes import page_routes

app = FastAPI(title="Facebook Insights Microservice")

@app.on_event("startup")
async def startup():
    await Database.connect()

@app.on_event("shutdown")
async def shutdown():
    await Database.disconnect()

app.include_router(page_routes.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,debug=True)