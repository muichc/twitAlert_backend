from flask import Flask, send_from_directory, jsonify, Blueprint, request
from.extensions import mongo

main = Blueprint('main', __name__)


@main.route('/')
def index():
    user_collection = mongo.db.users
    user_collection.insert({'name':'Anthony'})
    return '<h1>Added a User! </h1>'

# if __name__ == "__main__":
#     app.run()