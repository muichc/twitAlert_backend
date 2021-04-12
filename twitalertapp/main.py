from flask import Flask, send_from_directory, jsonify, Blueprint, request
from .extensions import mongo, flask_bcrypt, jwt
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)

main = Blueprint('main', __name__)

@main.route('/users', methods=["GET"])
def get_all_users():
    user_collection = mongo.db.users
    return jsonify(user_collection)

# @main.route('/')


