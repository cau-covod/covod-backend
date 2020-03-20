from flask import Flask
from flask_restful import Api
from covod.resources.foo import Foo

app = Flask(__name__)
api = Api(app)

api.add_resource(Foo, '/foo', '/foo/<string:id>')

api.init_app(app)
