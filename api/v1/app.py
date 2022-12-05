#!/usr/bin/python3
"""
Flask app module
"""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ closes the storage on teardown """
    storage.close()


if __name__ == '__main__':
    from os import getenv
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
