#!/usr/bin/python3
"""
module - places
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.state import State


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET'],
        strict_slashes=False)
def show_city_places(city_id):
    """
    Retrieves the list of all Place objects of a City:
    GET /api/v1/cities/<city_id>/places
    """
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify([place.to_dict() for place in city.places]), 200
    abort(404)


@app_views.route(
        '/places/<string:place_id>',
        methods=['GET'],
        strict_slashes=False)
def show_places(place_id):
    """
    Retrieves a Place object. : GET /api/v1/places/<place_id>
    """
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route(
        '/places/<string:place_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_place(palce_id):
    """
    Deletes a Place object: DELETE /api/v1/places/<place_id>
    """
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route(
        '/cities/<string:city_id>/places',
        methods=['POST'],
        strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place: POST /api/v1/cities/<city_id>/places
    """
    city = storage.get(City, city_id)
    if city is not None:
        json_data = request.get_json(silent=True)
        if json_data is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in json_data:
            abort(400, 'Missing user_id')
        user = storage.get(User, json_data['user_id'])
        if user is not None:
            if 'name' not in json_data:
                abort(400, 'Missing name')
            place = Place(**json_data)
            storage.new(place)
            storage.save()
            return jsonify(place), 201
        abort(404)
    abort(404)


@app_views.route(
        '/places/<string:place_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_palce(place_id):
    """
    Updates a Place object: PUT /api/v1/places/<place_id>
    """
    place = storage.get(Place, place_id)
    banned_attributes = (
            'id',
            'user_id',
            'city_id',
            'created_at',
            'updated_at')
    if place is not None:
        json_data = request.get_json(silent=True)
        if json_data is None:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in banned_attributes:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    POST /api/v1/places_search that retrieves all Place objects depending
    of the JSON in the body of the request.
    """
    def filter_place(place, amenities_ids):
        if amenities_ids:
            for amenity_id in place.amenity_ids:
                if amenity_id not in amenities_ids:
                    return False
        return True

    try:
        json_data = request.get_json()
        states_ids = set(json_data.get('states', []))
        cities_ids = set(json_data.get('cities', []))
        amenities_ids = set(json_data.get('amenities', []))
        if not states_ids and not cities_ids and not amenities_ids:
            places = set(
                    [place.to_dict()
                        for place in storage.all(Place).values()])
        else:
            for state_id in states_ids:
                state = storage.get(State, state_id)
                if state and state.cities:
                    cities_ids.update([city.id for city in state.cities])
            cities = set(
                    [storage.get(City, city_id)
                        for city_id in cities_ids])
            cities.discard(None)
            places = set()
            for city in cities:
                places.update(city.places)
            found_places = [
                    place for place in places
                    if filter_place(place, amenities_ids)]
            return jsonify([place.to_dict() for place in found_places]), 200
    except BadRequest:
        return jsonify({'error': 'Not a JSON'}), 400
