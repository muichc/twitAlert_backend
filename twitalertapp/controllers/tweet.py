from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from twitalertapp.extensions import mongo, jwt
from twitalertapp.tweets import tweet_main
from twitalertapp.service import get_location_name


tweet = Blueprint('tweet', __name__)

@tweet.route('/user/tweets', methods=["GET"])
@jwt_required(refresh=False, locations=['headers'])
def get_tweets():
    current_user_id = get_jwt_identity()
    try:
        location = get_location_name(current_user_id)
    except:
        return jsonify({"ok":False, "message":"Error retrieving location or updating user location"})
    try:
        tweets = tweet_main(location)
        return jsonify({"data": tweets}), 200
    except:
        return jsonify({"ok":False, "message":"Error retrieving tweets"})
    
    