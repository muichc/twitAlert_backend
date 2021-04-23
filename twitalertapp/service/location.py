from flask import jsonify, Blueprint, request as flask_request
from flask_jwt_extended import jwt_required, get_jwt_identity
from twitalertapp.extensions import mongo, flask_bcrypt, jwt, JSONEncoder
from twitalertapp.tweets import tweet_main
import requests
from requests.auth import HTTPBasicAuth
from twitalertapp.settings import ZIP_API_KEY2, ZIP_API_EMAIL2, ZIP_API_PASSWORD2


