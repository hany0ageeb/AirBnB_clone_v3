#!/usr/bin/python3
"""
module - states
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


__banned_attributes = ('id', 'created_at', 'updated_at')


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route(
        '/states/<string:state_id>',
        methods=['GET'],
        strict_slashes=False)
def show_states(state_id=None):
    """
    handle route: /api/v1/states
    """
    if state_id:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict()), 200
        else:
            abort(404)
    else:
        states = storage.all(State).values()
        result = [state.to_dict() for state in states]
        return jsonify(result), 200


@app_views.route(
        '/states/<string:state_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_state(state_id):
    """
    handle route: /api/v1/states/<state_id> - DELETE
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        '/states',
        methods=['POST'],
        strict_slashes=False)
def create_state():
    """Creates a State: POST /api/v1/states"""
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_data.keys():
        abort(400, 'Missing name')
    state = State(**json_data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route(
        '/states/<string:state_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object: PUT /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        json_data = request.get_json(silent=True)
        if json_data is None:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in __banned_attributes:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
