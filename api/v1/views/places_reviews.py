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
    for i in storage.all("Place").values():
        if i.id == place_id:
            nrv = request.get_json(silent=True)
            if nrv is None:
                abort(400, 'Not a JSON')
            if 'user_id' not in nrv.keys():
                abort(400, 'Missing user_id')
            if 'text' not in nrv.keys():
                abort(400, 'Missing text')
            tmp_list = []
            for i in storage.all("User").values():
                tmp_list.append(i.id)
            for key, value in nrv.items():
                if key == 'user_id':
                    if value not in tmp_list:
                        abort(404)
            nrv["place_id"] = place_id
            my_review = Review(**nrv)
            storage.new(my_review)
            storage.save()
            return jsonify(my_review.to_dict()), 201
    abort(404)


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
