import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URI = os.getenv('MONGODB_URI')
JWT_SECRET_KEY = os.getenv('SECRET')
ZIP_API_KEY = os.getenv('ZIP_API')
ZIP_API_EMAIL = os.getenv('ZIP_API_EMAIL')
ZIP_API_PASSWORD = os.getenv('ZIP_API_PASSWORD')
ZIP_API_KEY2 = os.getenv('ZIP_API2')
ZIP_API_EMAIL2 = os.getenv('ZIP_API_EMAIL2')
ZIP_API_PASSWORD2 = os.getenv('ZIP_API_PASSWORD2')