from flask import Flask
from .extensions import mongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from .main import main
import datetime

def create_app(config_object='twitalertapp.settings'):
    app = Flask(__name__)
    
    app.config.from_object(config_object)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=7)

    mongo.init_app(app)
    jwt = JWTManager(app)
    flask_bcrypt = Bcrypt(app)

    app.register_blueprint(main)

    return app