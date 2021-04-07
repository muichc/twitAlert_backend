import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URI = os.getenv('MONGODB_URI')
JWT_SECRET_KEY=os.getenv('SECRET')