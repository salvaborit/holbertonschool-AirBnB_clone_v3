#!/usr/bin/python3
"""
Module state
"""
from api.v1.views import app_views
from flask import abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
    """ retrieves all states """
    states_return = []
    for state in storage.all('State').values():
        states_return.append(state.to_dict())
    return states_return


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_state_by_id(state_id):
    """ retrieves state by id for GET, DELETE """
    for state in storage.all('State').values():
        if state.id == state_id:
            if request.method == 'GET':
                return state.to_dict()
            elif request.method == 'DELETE':
                storage.delete(state)
                storage.save()
                return {}, 200
    abort(404)

@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """ creates a state """
    http_request = request.get_json(silent=True)
    if http_request is None:
        abort(400, 'Not a JSON')
    elif 'name' not in http_request.keys():
        abort(400, 'Missing name')
    else:
        new_state = State(**http_request)
        storage.new(new_state)
        storage.save()
        return new_state.to_dict(), 201

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_state(state_id):
    """ updates a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    http_request = request.get_json(silent=True)
    if http_request is None:
        abort(400, 'Not a JSON')
    for key, val in http_request.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(state, key, val)
    storage.save()
    return state.to_dict(), 200
