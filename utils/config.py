import os
from pathlib import Path
from dotenv import load_dotenv


# Get the path of the utils folder
BASE_DIR = Path(__file__).resolve().parent


# Load the .env file from the utils folder
load_dotenv(BASE_DIR / ".env")


# Get API keys from .env
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")