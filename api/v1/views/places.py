#!/usr/bin/python3
"""
Module places
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
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


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
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
