#!/usr/bin/python3
"""
Module cities
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def states_cities(state_id):
    """ retrieves all cities linked to a state """
    if storage.get(State, state_id) is None:
        abort(404)
    cities = []
    for city in storage.all('City').values():
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_city(city_id):
    """ retrieves city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
