#!/usr/bin/python3
"""
Flask app module
"""
from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views
HOST = getenv('HBNB_API_HOST', '0.0.0.0')
PORT = getenv('HBNB_API_PORT', '5000')


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ closes the storage on teardown """
    storage.close()


if __name__ == '__main__':
    app.run(host=HOST,
            port=PORT,
            threaded=True,
            debug=True)
