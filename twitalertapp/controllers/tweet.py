from flask import jsonify, Blueprint, request as flask_request
from flask_jwt_extended import jwt_required, get_jwt_identity
from twitalertapp.extensions import mongo, flask_bcrypt, jwt, JSONEncoder
from twitalertapp.tweets import tweet_main
import requests
from requests.auth import HTTPBasicAuth
from twitalertapp.settings import ZIP_API_KEY, ZIP_API_EMAIL, ZIP_API_PASSWORD

tweet = Blueprint('tweet', __name__)

@tweet.route('/user/tweets', methods=["GET"])
@jwt_required(refresh=False, locations=['headers'])
def get_tweets():
    current_user_id = get_jwt_identity()
    current_user = mongo.db.users.find_one({'_id': current_user_id})
    if current_user["locationName"]:
        print(current_user["locationName"])
        location = current_user["locationName"]
    else:
        zip_url = f"https://service.zipapi.us/zipcode/{current_user['location']}?X-API-KEY={ZIP_API_KEY}"
        response = requests.get(zip_url, auth=HTTPBasicAuth(ZIP_API_EMAIL, ZIP_API_PASSWORD))
        response_json = response.json()
        try:
            location = response_json["data"]["city"]
            current_user["locationName"] = location
        except:
            return jsonify({"ok":False, "message":"Error retrieving location or tweets"})
    try:
        tweets = tweet_main(location)
        print("LENGTH OF TWEETS WE GOT IS ", len(tweets), " AND THE TWEETS ARE >>>>>", tweets)
        return jsonify({"data": tweets}), 200
    except:
        return jsonify({"ok":False, "message":"Error retrieving tweets"})
    
    