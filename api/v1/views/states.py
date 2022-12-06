#!/usr/bin/python3
"""
Module state
"""
from api.v1.views import app_views


@app_views.route('/states')
def get_all_states():
    """ retrieves all states """
    from models import storage
    states_return = []
    for state in storage.all('State').values():
        states_return.append(state.to_dict())
    return states_return
