#!/usr/bin/python3
"""
Module users
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ retrieves all users """
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route(
    '/users/<user_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_user_by_id(user_id):
    """ retrieves user by id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """ posts a user """
    req = request.get_json(silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    elif 'email' not in req.keys():
        abort(400, 'Missimg email')
    elif 'password' not in req.keys():
        abort(400, 'Missimg password')
    else:
        new_user = User(**req)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_user(user_id):
    """ updates user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    req = request.get_json(silent=True)
    if req is None:
        abort(400, 'Not a JSON')
    for key, val in req.items():
        if key == 'id' or key == 'email' or \
                key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200
