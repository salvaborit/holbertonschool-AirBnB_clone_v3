#!/usr/bin/python3
"""
Module index
"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ retrieves api status """
    return {'status': 'OK'}


@app_views.route('/stats')
def stats():
    """ retrieves number of objects by type """
