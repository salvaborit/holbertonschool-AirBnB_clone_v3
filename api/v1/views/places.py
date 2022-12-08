#!/usr/bin/python3
"""
Module places
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_places_in_city(city_id):
    """ retrieves all places in a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in storage.all('Place').values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_place(place_id):
    """ retrieves a place by id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def post_place(city_id):
    """ posts place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json(silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in req.keys():
        abort(400, 'Missing user_id')
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    if 'name' not in req.keys():
        abort(400, 'Missing name')
    new_place = Place(**req)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_place(place_id):
    """ updates a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json(silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    for key, val in req.items():
        if key == 'id' or key == 'user_id' or key == 'city_id' or \
                key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(place, key, val)
    return jsonify(place.to_dict()), 200
