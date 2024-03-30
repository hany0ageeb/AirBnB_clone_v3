#!/usr/bin/python3
"""
module - places_reviews
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
        '/places/<string:place_id>/reviews',
        methods=['GET'],
        strict_slashes=False)
def show_place_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place:
    GET /api/v1/places/<place_id>/reviews
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(place_reviews), 200


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['GET'],
        strict_slashes=False)
def show_reviews(review_id):
    """
    Retrieves a Review object. : GET /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object: DELETE /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<string:place_id>/reviews',
        methods=['POST'],
        strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review: POST /api/v1/places/<place_id>/reviews
    1. You must use request.get_json from Flask
    2. If the place_id is not linked to any Place object, raise a 404 error
    3. If the HTTP body request is not valid JSON,
       raise a 400 error with the message Not a JSON
    4. If the dictionary doesn’t contain the key user_id,
       raise a 400 error with the message Missing user_id
    5. If the user_id is not linked to any User object,
       raise a 404 error
    6. If the dictionary doesn’t contain the key text,
       raise a 400 error with the message Missing text
    7. Returns the new Review with the status code 201
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_data:
        abort(400, 'Missing user_id')
    user_id = json_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in json_data:
        abort(400, 'Missing text')
    json_data['place_id'] = place_id
    review = Review(**json_data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object: PUT /api/v1/reviews/<review_id>
    1. If the review_id is not linked to any Review object, raise a 404 error
    2. You must use request.get_json from Flask
    3. If the HTTP request body is not valid JSON,
       raise a 400 error with the message Not a JSON
    4. Update the Review object with all key-value pairs of the dictionary
    5. Ignore keys: id, user_id, place_id, created_at and updated_at
    6. Returns the Review object with the status code 200
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, 'Not a JSON')
    ignore_keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    for key in ignore_keys:
        json_data.pop(key, None)
    for key, value in json_data.items():
        setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
