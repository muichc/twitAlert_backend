from flask import jsonify
from twitalertapp.extensions import mongo
import requests
from requests.auth import HTTPBasicAuth
from twitalertapp.settings import ZIP_API_KEY2, ZIP_API_EMAIL2, ZIP_API_PASSWORD2


def get_location_name(user_id):
    user = mongo.db.users.find_one({'_id': user_id})
    location_key = "locationName"
    if location_key in user:
        location = user["locationName"]
        return location
    else:
        zip_url = f"https://service.zipapi.us/zipcode/{user['location']}?X-API-KEY={ZIP_API_KEY2}"
        response = requests.get(zip_url, auth=HTTPBasicAuth(ZIP_API_EMAIL2, ZIP_API_PASSWORD2))
        response_json = response.json()
        location = response_json["data"]["city"]
        mongo.db.users.update({
            '_id': user_id
        }, 
        {   '$set': {
                'locationName': location
            }
        })
        return location
        
