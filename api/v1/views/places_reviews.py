#!/usr/bin/python3
"""
Module places_reviews
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def get_reviews_by_place(place_id):
    """ retrieves reviews by place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in storage.all('Review').values():
        if review.place_id == place_id:
            reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route(
    '/reviews/<review_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_review(review_id):
    """ retrieves review by id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def post_review(place_id):
    """ posts a review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json(silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in req.keys():
        abort(400, 'Missing user_id')
    if 'text' not in req.keys():
        abort(400, 'Missing text')
    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)
    req['place_id'] == place_id
    new_review = Review(**req)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def put_review(review_id):
    """ updates review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    req = request.get_json(silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    for key, val in req.items():
        if key == 'id' or key == 'user_id' or key == 'place_id' or \
                key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(review, key, val)
    storage.save()
    return jsonify(review.to_dict()), 200
