from flask import Flask, send_from_directory, jsonify, Blueprint
from.extensions import mongo

# from flask_mongoengine import MongoEngine
# from flask_pymongo import PyMongo
# from dotenv import load_dotenv
# import os
# load_dotenv()

# app = Flask(__name__, static_folder='static', static_url_path='')
# DB_URI = os.getenv('MONGODB_URI')
# # app.config['MONGODB_HOST'] = DB_URI
# # cluster = MongoClient(DB_URI)
# # db = cluster["test"]
# # collection = db["test"]
# app.config["MONGO_URI"] = DB_URI
# mongo = PyMongo(app)

# post = {"_id": 0, "name": "tim", "score":5}

# mongo.insert_one(post)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    user_collection = mongo.db.users
    user_collection.insert({'name':'Anthony'})
    return '<h1>Added a User! </h1>'

if __name__ == "__main__":
    app.run()