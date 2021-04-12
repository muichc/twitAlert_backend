from flask import jsonify, Blueprint, request as flask_request
from flask_jwt_extended import jwt_required, get_jwt_identity
from twitalertapp.extensions import mongo, flask_bcrypt, jwt, JSONEncoder
from twitalertapp.tweets import tweet_main
import requests
from requests.auth import HTTPBasicAuth
from twitalertapp.settings import ZIP_API_KEY2, ZIP_API_EMAIL2, ZIP_API_PASSWORD2

tweet = Blueprint('tweet', __name__)

@tweet.route('/user/tweets', methods=["GET"])
@jwt_required(refresh=False, locations=['headers'])
def get_tweets():
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({'_id': current_user_id})
    location_key = "locationName"
    if location_key in current_user:
        location = current_user["locationName"]
    else:
        zip_url = f"https://service.zipapi.us/zipcode/{current_user['location']}?X-API-KEY={ZIP_API_KEY2}"
        response = requests.get(zip_url, auth=HTTPBasicAuth(ZIP_API_EMAIL2, ZIP_API_PASSWORD2))
        response_json = response.json()
        try:
            location = response_json["data"]["city"]
            mongo.db.users.update({
                '_id': current_user_id
            }, 
            {
                '$set': {
                    'locationName': location
                }
            })
            updated_user = mongo.db.users.find_one({'_id': current_user_id})
        except:
            return jsonify({"ok":False, "message":"Error retrieving location or tweets"})
    try:
        tweets = tweet_main(location)
        return jsonify({"data": tweets}), 200
    except:
        return jsonify({"ok":False, "message":"Error retrieving tweets"})
    
    