#!/usr/bin/python3
"""
Module app
"""
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    """ closes storage on teardown """
    storage.close()


@app.errorhandler(404)
def handler_404(error):
    """ 404 not found error handler """
    return dict(error='Not found'), 404


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'),
            threaded=True,
            debug=True)
