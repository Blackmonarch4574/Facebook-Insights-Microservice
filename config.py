from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    MONGODB_URL: str = Field(..., env='MONGODB_URL')
    DATABASE_NAME: str = 'facebook_insights'
    OPENAI_API_KEY: str = Field(..., env='OPENAI_API_KEY')
    REDIS_URL: str = Field(..., env='REDIS_URL')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()