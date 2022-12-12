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


@app_views.route(
    '/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
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


@app_views.route(
    '/places/<place_id>', strict_slashes=False, methods=['GET', 'DELETE'])
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


@app_views.route(
    '/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def post_place(city_id):
    """ posts place """
    for i in storage.all("City").values():
        if i.id == city_id:
            npl = request.get_json(silent=True)
            if npl is None:
                abort(400, 'Not a JSON')
            if 'user_id' not in npl.keys():
                abort(400, 'Missing user_id')
            if 'name' not in npl.keys():
                abort(400, 'Missing name')
            tmp_list = []
            for i in storage.all("User").values():
                tmp_list.append(i.id)
            for key, value in npl.items():
                if key == 'user_id':
                    if value not in tmp_list:
                        abort(404)
            npl["city_id"] = city_id
            my_place = Place(**npl)
            storage.new(my_place)
            storage.save()
            return jsonify(my_place.to_dict()), 201
    abort(404)


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
    storage.save()
    return jsonify(place.to_dict()), 200
