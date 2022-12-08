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


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """ retrieves city by id """
    for city in storage.all('City').values():
        if city.id == city_id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def city_delete(city_id):
    """Delete a city"""
    for i in storage.all("City").values():
        if i.id == city_id:
            my_city = storage.all()["City" + '.' + city_id]
            storage.delete(my_city)
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Create a new city"""
    for i in storage.all("State").values():
        if i.id == state_id:
            nct = request.get_json(silent=True)
            if nct is None:
                abort(400, 'Not a JSON')
            if 'name' not in nct.keys():
                abort(400, 'Missing name')
            nct["state_id"] = state_id
            my_city = City(**nct)
            storage.new(my_city)
            storage.save()
            return jsonify(my_city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Update a city"""
    uct = request.get_json(silent=True)
    if uct is None:
        abort(400, 'Not a JSON')
    for i in storage.all("City").values():
        if i.id == city_id:
            my_city = storage.all()["City" + '.' + city_id]
            for key, value in uct.items():
                if key == 'id' or key == 'created_at' \
                   or key == 'updated_at':
                    pass
                else:
                    setattr(my_city, key, value)
            storage.save()
            return jsonify(my_city.to_dict()), 200
    abort(404)
