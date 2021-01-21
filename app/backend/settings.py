import os
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")

# These values of True or False should not be in the settings.py but rather in the .env, 
# as they will change when we move to production, so we'll load the updating values from .env
DEBUG = True
TESTING = True
