from flask import Flask
from flask_env import MetaFlaskEnv
from flask_cors import CORS

from covod.models.models import db
from covod.oauth2 import setup_oauth
from covod.blueprints import api, oauth2, web_app
from covod.resources.lecture import storage


class Configuration(metaclass=MetaFlaskEnv):
    ENV_LOAD_ALL = True


app = Flask(__name__, static_url_path="/web-app")
app.config.from_object(Configuration)
CORS(app)

app.register_blueprint(api.bp)
app.register_blueprint(oauth2.bp)
app.register_blueprint(web_app.bp)


@app.cli.command("insert-dummy-data")
def insert_dummy_data():
    exec(open("admin/insert-dummy-data.py").read())


@app.before_first_request
def create_tables():
    db.create_all()

db.init_app(app)
setup_oauth(app)
storage.init_app(app)
