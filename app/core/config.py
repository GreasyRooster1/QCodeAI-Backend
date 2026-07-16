import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DEFAULT_MODEL: str = "llama3"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    FIREBASE_SERVICE_ACCOUNT_PATH: str = "service-account.json"
    
    class Config:
        env_file: str = ".env"

settings = Settings()