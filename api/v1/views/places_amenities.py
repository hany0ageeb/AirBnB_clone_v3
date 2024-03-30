#!/usr/bin/python3
"""
Module  - places_amenities
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from werkzeug.exceptions import BadRequest
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route(
        '/places/<string:place_id>/amenities',
        methods=['GET'],
        strict_slashes=False)
def list_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place:
    GET /api/v1/places/<place_id>/amenities
    """
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify([amenity.to_dict() for amenity in place.amenities]), 200
    abort(404)


@app_views.route(
        '/places/<string:place_id>/amenities/<string:amenity_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_amenity_of_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is not None:
            if place.remove_amenity(amenity):
                storage.save()
                return jsonify({}), 200
            abort(404)
        abort(404)
    abort(404)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'],
        strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Link a Amenity object to a Place:
    POST /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    place = storage.get(Place, place_id)
    if place is not None:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is not None:
            if place.add_amenity(amenity):
                storage.save()
                return jsonify(amenity.to_dict()), 201
            return jsonify(amenity.to_dict()), 200
        abort(404)
    abort(404)
