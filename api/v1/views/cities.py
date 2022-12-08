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
    for state in storage.all('State').values():
        if state.id == state_id:
            cities = []
            if state.cities:
                for city in storage.all('City').values():
                    if city.state_id == state_id:
                        cities.append(city.to_dict())
            return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_city(city_id):
    """ retrieves city by id """
    for city in storage.all('City').values():
        if city.id == city_id:
            return jsonify(city.to_dict())
    abort(404)
