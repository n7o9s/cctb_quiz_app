from os import getenv
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    """Base configuration."""
    DEBUG = False
    MONGO_URI = getenv("MONGO_URI", "")
    MONGO_DATABASE = getenv("MONGO_DATABASE", "")

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    MONGO_URI = getenv("MONGO_URI", "")