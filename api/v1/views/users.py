#!/usr/bin/python3
"""
module - users
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route(
        '/users/<string:user_id>',
        methods=['GET'],
        strict_slashes=False)
def show_users(user_id=None):
    """
    Retrieves the list of all User objects: GET /api/v1/users
    Retrieves a User object: GET /api/v1/users/<user_id>
    """
    if user_id is None:
        result = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(result), 200
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict()), 200
    abort(404)


@app_views.route(
        '/users/<string:user_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object:: DELETE /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route(
        '/users',
        methods=['POST'],
        strict_slashes=False)
def create_user():
    """
    Creates a User: POST /api/v1/users
    """
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'email' not in json_data:
        abort(400, 'Missing email')
    if 'password' not in json_data:
        abort(400, 'Missing password')
    user = User(**json_data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
        '/users/<string:user_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object: PUT /api/v1/users/<user_id>
    """
    user = storage.get(User, user_id)
    ignore_keyes = ('id', 'email', 'created_at', 'updated_at')
    if user is not None:
        json_data = request.get_json(silent=True)
        if json_data is None:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in ignore_keyes:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    abort(404)
