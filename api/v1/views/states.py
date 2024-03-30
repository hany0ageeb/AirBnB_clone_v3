#!/usr/bin/python3
"""
module - states
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from models import storage
from models.state import State


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
        states = storage.all(State)
        states = list(map(lambda state: state.to_dict(), states.values()))
        return jsonify(states), 200


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
        state.delete()
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
    try:
        json_data = request.get_json()
        if 'name' not in json_data.keys():
            return jsonify({'error': 'Missing name'}, status=400)
        state = State(**json_data)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route(
        '/states/<string:state_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object: PUT /api/v1/states/<state_id>
    """
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        else:
            json_data = request.get_json()
            for key, value in json_data.items():
                if key not in ('id', 'created_at', 'update_at'):
                    setattr(state, key, value)
            storage.save()
            return jsonify(state.to_dict()), 200
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400
