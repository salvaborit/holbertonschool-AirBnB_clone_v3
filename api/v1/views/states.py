#!/usr/bin/python3
"""
Module states
"""
from flask import abort, request
from api.v1.views import app_views
from models import storage



@app_views.route('/states')
def get_all_states():
    """ retrieves all states """
    states_return = []
    for state in storage.all('State').values():
        states_return.append(state.to_dict())
    return states_return

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def get_state_by_id(state_id):
    """ retrieves state by id """
    for state in storage.all('State').values():
        if state.id == state_id:
            if request.method == 'GET':
                return state.to_dict()
            elif request.method == 'DELETE':
                storage.delete(state)
    abort(404)
