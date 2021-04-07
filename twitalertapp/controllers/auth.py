from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from twitalertapp.extensions import mongo, flask_bcrypt, jwt, JSONEncoder
from ..user import validate_user

auth = Blueprint('auth', __name__)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok':False,
        'message': 'Missing Authorization Header'
    }), 401

@auth.route('/auth/login', methods=["POST"])
def login():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email':data['email']}) 
        user["_id"] = str(user["_id"])
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=str(user["_id"]))
            user['token'] = access_token
            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@auth.route('/auth/register', methods=["POST"])
def register():
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email':data['email']})
        if not user:
            data['password'] = flask_bcrypt.generate_password_hash(data['password'])
            mongo.db.users.insert_one(data)
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
        else:
            return jsonify({'ok':False, 'message': 'User already exists'})
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@auth.route('/user', methods=['GET', 'DELETE', 'PUT'])
@jwt_required(refresh=False, locations=['headers'])
def user():
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query, {"_id": 0})
        if data:
            del data['password']
        # data["_id"] = str(data["_id"])
        return jsonify({'ok': True, 'data': data}), 200

    data = request.get_json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PUT':
        user_info=request.args
        if data.get('payload', {}) != {}:
            mongo.db.users.update_one(
                user_info, {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

