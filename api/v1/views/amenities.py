#!/usr/bin/python3
"""
Module amenities
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """ retrieves all amenities """
    amenities = []
    for amenity in storage.all('Amenity').values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_amenity_by_id(amenity_id):
    """ retrieves amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """ posts an amenity """
    req = request.get_json(silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    elif 'name' not in req.keys():
        abort(400, 'Missing name')
    else:
        new_amenity = Amenity(**req)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


# @app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
# def put_amenity(amenity_id):
#     """ updates an amenity """
