from flask import Flask
from flask_env import MetaFlaskEnv

from covod.models.models import db
from covod.oauth2 import setup_oauth
from covod.blueprints import api, oauth2
from covod.resources.lecture import storage


class Configuration(metaclass=MetaFlaskEnv):
    ENV_LOAD_ALL = True


app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(api.bp)
app.register_blueprint(oauth2.bp)


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)
setup_oauth(app)
storage.init_app
