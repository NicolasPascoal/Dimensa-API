import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    IPWHOIS_API_KEY = os.getenv("IPWHOIS_API_KEY")
    SECRET_TOKEN = os.getenv("SECRET_TOKEN")
    REDIS_URL = os.getenv("REDIS_URL")