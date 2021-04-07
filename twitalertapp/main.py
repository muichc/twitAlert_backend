from flask import Flask, send_from_directory, jsonify, Blueprint, request
from .extensions import mongo, flask_bcrypt, jwt
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity)
from .user import validate_user




main = Blueprint('main', __name__)


@main.route('/users', methods=["GET"])
def get_all_users():
    user_collection = mongo.db.users
    return jsonify(user_collection)

# @main.route('/auth/login', methods=["POST"])
# def login():
#     data = validate_user(request.get_json())
#     if data['ok']:
#         data = data['data']
#         user = mongo.db.users.find_one({'email':data['email']})
#         if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
#             access_token = create_access_token(identity=data)
#             refresh_token = create_refresh_token(identity=data)
#             user['token'] = access_token
#             return jsonify({'ok': True, 'data': user}), 200
#         else:
#             return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
#     else:
#         return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


# @main.route('/auth/register', methods=["POST"])
# def register():
#     data = validate_user(request.get_json())
#     if data['ok']:
#         data = data['data']
#         data['password'] = flask_bcrypt.generate_password_hash(data['password'])
#         mongo.db.users.insert_one(data)
#         return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
#     else:
#         return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


# @main.route('/user', methods=['GET', 'DELETE', 'PUT'])
# @jwt_required
# def user():
#     if request.method == 'GET':
#         query = request.args
#         data = mongo.db.users.find_one(query, {"_id": 0})
#         return jsonify({'ok': True, 'data': data}), 200

#     data = request.get_json()
#     if request.method == 'DELETE':
#         if data.get('email', None) is not None:
#             db_response = mongo.db.users.delete_one({'email': data['email']})
#             if db_response.deleted_count == 1:
#                 response = {'ok': True, 'message': 'record deleted'}
#             else:
#                 response = {'ok': True, 'message': 'no record found'}
#             return jsonify(response), 200
#         else:
#             return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

#     if request.method == 'PUT':
#         if data.get('query', {}) != {}:
#             mongo.db.users.update_one(
#                 data['query'], {'$set': data.get('payload', {})})
#             return jsonify({'ok': True, 'message': 'record updated'}), 200
#         else:
#             return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


