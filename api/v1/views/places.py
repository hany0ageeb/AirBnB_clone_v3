#!/usr/bin/python3
"""
module - places
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
        '/cities/<string:city_id>/places',
        methods=['GET'],
        strict_slashes=False)
def show_city_places(city_id):
    """
    Retrieves the list of all Place objects of a City:
    GET /api/v1/cities/<city_id>/places
    """
    city = storage.get(City, city_id)
    if city:
        city_places = [place.to_dict() for place in city.places]
        return jsonify(city_places), 200
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
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route(
        '/places/<string:place_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object: DELETE /api/v1/places/<place_id>
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<string:city_id>/places',
        methods=['POST'],
        strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place: POST /api/v1/cities/<city_id>/places
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, json_data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in json_data:
        abort(400, 'Missing name')
    json_data['city_id'] = city_id
    place = Place(**json_data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


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
    if place is None:
        abort(404)
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')
    for key, value in json_data.items():
        if key not in banned_attributes:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route(
        '/places_search',
        methods=['POST'],
        strict_slashes=False)
def search_places():
    """
    POST /api/v1/places_search that retrieves all Place objects depending
    of the JSON in the body of the request.
    """
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')
    states_ids = set(json_data.get('states', []))
    cities_ids = set(json_data.get('cities', []))
    amenities_ids = set(json_data.get('amenities', []))
    if states_ids:
        states_cities = [
                city.id
                for city in storage.all(City).values()
                if city.state_id in states_ids]
        cities_ids.update(states_cities)
    if cities_ids:
        places = [
                place
                for place in storage.all(Place).values()
                if place.city_id in cities_ids]
    else:
        places = storage.all(Place).values()
    if amenities_ids:
        places = [
                place
                for place in places
                if amenities_ids.issubset(set(place.amenity_ids))]
    return jsonify([place.to_dict() for place in places]), 200
