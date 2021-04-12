from flask import Flask, jsonify
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_registration_schema = {
    "type":"object",
    "properties":{
        "username": {
            "type":"string",
        },
        "email": {
            "type":"string",
            "format":"email"
        },
        "password": {
            "type":"string",
            "minLength": 5
        },
        "location": {
            "type":"integer",
            "minLength":5
        }
    },
    "required": ["email", "password", "username", "location"],
    "additionalProperties":False
}

user_login_schema = {
    "type":"object",
    "properties":{
        "email": {
            "type":"string",
            "format":"email"
        },
        "password": {
            "type":"string",
            "minLength": 5
        },
    },
    "required": ["email", "password"],
    "additionalProperties":False
}

# Not doing anything with this right now, but for future purposes
user_login_schema = {
    "type":"object",
    "properties":{
        "firstName": {
            "type":"string",
        },
        "lastName": {
            "type":"string",
        },
        "username": {
            "type":"string",
        },
        "email": {
            "type":"string",
            "format":"email"
        },
        "password": {
            "type":"string",
            "minLength": 5
        },
        "location": {
            "type":"integer",
            "minLength":5
        },
        "locationName": {
            "type":"string",
        }
    },
    "additionalProperties":False
}


def validate_user_registration(data):
    try:
        validate(data, user_registration_schema)
    except ValidationError as error:
        return {'ok': False, 'message':error}
    except SchemaError as error:
        return {'ok': False, 'message':error}
    return {'ok':True, 'data':data}

def validate_user_login(data):
    try:
        validate(data, user_login_schema)
    except ValidationError as error:
        return {'ok': False, 'message':error}
    except SchemaError as error:
        return {'ok': False, 'message':error}
    return {'ok':True, 'data':data}
