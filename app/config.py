from os import getenv
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    """Base configuration class."""
    DEBUG = False
    MONGO_URI = getenv("MONGO_URI", "mongodb://localhost:27017")  # Default value
    MONGO_DATABASE = getenv("MONGO_DATABASE", "quizdb")  # Default database name

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    MONGO_URI = getenv("MONGO_URI", "mongodb://localhost:27017")  # Default for local development
    MONGO_DATABASE = getenv("MONGO_DATABASE", "quizdb")  # Default for local development