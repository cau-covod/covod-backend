from flask import Flask
from flask_env import MetaFlaskEnv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from covod.resources.foo import Foo

class Configuration(metaclass=MetaFlaskEnv):
    ENV_LOAD_ALL = True

app = Flask(__name__)
app.config.from_object(Configuration)

api = Api(app)
db = SQLAlchemy(app)

api.add_resource(Foo, '/foo', '/foo/<string:id>')

api.init_app(app)
