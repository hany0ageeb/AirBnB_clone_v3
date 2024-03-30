#!/usr/bin/python3
"""
module - cities
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from werkzeug.exceptions import BadRequest
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        '/states/<string:state_id>/cities',
        methods=['GET'],
        strict_slashes=False)
def show_state_cities(state_id):
    """
    Retrieves the list of all City objects of a State:
    GET /api/v1/states/<state_id>/cities
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify([city.to_dict() for city in state.cities]), 200


@app_views.route(
        '/cities/<string:city_id>',
        methods=['GET'],
        strict_slashes=False)
def show_city(city_id):
    """
    Retrieves a City object. : GET /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict()), 200


@app_views.route(
        '/cities/<string:city_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object: DELETE /api/v1/cities/<city_id>
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route(
        '/states/<string:state_id>/cities',
        methods=['POST'],
        strict_slashes=False)
def create_city(state_id):
    """
    Creates a City: POST /api/v1/states/<state_id>/cities
    """
    state = storage.get(State, state_id)
    if state is not None:
        try:
            json_data = request.get_json()
            if 'name' not in json_data:
                return jsonify({'error': 'Missing name'}), 400
            json_data['state_id'] = state_id
            city = City(**json_data)
            storage.new(city)
            storage.save()
            return jsonify(city.to_dict()), 201
        except BadRequest:
            return jsonify({'error': 'Not a JSON'}), 400
    else:
        abort(404)


@app_views.route(
        '/cities/<string:city_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object: PUT /api/v1/cities/<city_id>
    """
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            for key, value in json_data.items():
                if key not in ('id', 'update_at', 'created_at'):
                    setattr(city, key, value)
            storage.save()
            return jsonify(city.to_dict()), 200
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400
