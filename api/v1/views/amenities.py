#!/usr/bin/python3
"""
module - amenities
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from werkzeug.exceptions import BadRequest
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route(
        '/amenities/<string:amenity_id>',
        methods=['GET'],
        strict_slashes=False)
def show_amenities(amenity_id=None):
    """
    Retrieves the list of all Amenity objects: GET /api/v1/amenities
    Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>
    """
    if amenity_id is None:
        amenities = storage.all(Amenity)
        return jsonify(
                [amenity.to_dict() for amenity in amenities.values()]), 200
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is not None:
            return jsonify(amenity.to_dict()), 200
        abort(404)


@app_views.route(
        '/amenities/<string:amenity_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a Amenity: POST /api/v1/amenities
    """
    try:
        json_data = request.get_json()
        if 'name' not in json_data:
            return jsonify({'error': 'Missing name'}), 400
        amenity = Amenity(**json_data)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400


@app_views.route(
        '/amenities/<string:amenity_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_amenity():
    """
    Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        try:
            json_data = request.get_json()
            for key, value in json_data.items():
                if key not in ('id', 'created_at', 'updated_at'):
                    setattr(amenity, key, value)
            storage.save()
            return jsonify(amenity.to_dict()), 200
        except BadRequest:
            return jsonify({'error': 'Not a JSON'}), 400
    abort(404)
