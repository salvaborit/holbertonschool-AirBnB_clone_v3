#!/usr/bin/python3
"""
Module cities
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def cities_by_City(state_id):
    """List all cities in the City"""
    for i in storage.all("State").values():
        if i.id == state_id:
            my_state = storage.all()["State" + '.' + state_id]
            my_list = []
            if my_state.cities:
                for i in storage.all("City").values():
                    if i.state_id == state_id:
                        my_list.append(i.to_dict())
            return jsonify(my_list)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_by_id(city_id):
    """Return city by id"""
    for i in storage.all("City").values():
        if i.id == city_id:
            my_city = storage.all()["City" + '.' + city_id]
            return jsonify(my_city.to_dict())
    abort(404)
