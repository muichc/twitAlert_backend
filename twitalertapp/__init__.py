from flask import Flask
from .extensions import mongo, jwt, flask_bcrypt, cors
from .main import main
import datetime


config_object='twitalertapp.settings'

app = Flask(__name__)

app.config.from_object(config_object)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=7)

mongo.init_app(app)
jwt.init_app(app)
flask_bcrypt.init_app(app)
cors.init_app(app)


app.register_blueprint(main)

from . import controllers
app.register_blueprint(controllers.auth)
app.register_blueprint(controllers.tweet)




