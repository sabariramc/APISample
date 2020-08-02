from flask import Flask, current_app, jsonify
from uuid import uuid4
import os

from .utility import json_serializer

from .api import api_blueprint
from .db import init_db_command, close_db


class App(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)
        self.api_key = set()


def get_api_key():
    new_api_key = uuid4().hex
    current_app.api_key.add(new_api_key)
    return jsonify({'apiKey': new_api_key})


def create_app():
    app = App()
    app.config.from_mapping(
        SECRET_KEY=uuid4().hex,
        DATABASE=os.path.join(app.instance_path, 'appdata.sqlite'),
        SERVER_NAME=os.environ.get("FLASK_SERVER_NAME", None),
        RESTFUL_JSON={"default": json_serializer}
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.before_first_request(init_db_command)

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.add_url_rule('/getapikey', 'get_api_key', get_api_key, methods=['GET'])

    app.teardown_request(close_db)

    @app.errorhandler(404)
    def not_found(e):
        return {"status": "ERROR", "errorCode": "path-not-found"}, 404

    @app.errorhandler(500)
    def internal_error(e):
        return {"status": "ERROR", "errorCode": "unhandled-error"}, 500

    return app
