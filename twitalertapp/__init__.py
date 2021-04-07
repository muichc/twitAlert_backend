from flask import Flask
from .extensions import mongo, jwt, flask_bcrypt
from .main import main
import datetime
import json
from bson.objectid import ObjectId


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

config_object='twitalertapp.settings'

app = Flask(__name__)

app.config.from_object(config_object)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=7)

mongo.init_app(app)
jwt.init_app(app)
flask_bcrypt.init_app(app)


app.register_blueprint(main)
from . import controllers
app.register_blueprint(controllers.auth)




