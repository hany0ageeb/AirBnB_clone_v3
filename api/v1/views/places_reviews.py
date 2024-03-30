#!/usr/bin/python3
"""
module - places_reviews
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from werkzeug.exceptions import BadRequest
from models import storage
from models.place import Place
from models.review import Review


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
    if place is not None:
        return jsonify([review.to_dict() for review in place.reviews]), 200
    abort(404)


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['GET'],
        strict_slashes=False)
def show_reviews(review_id):
    """
    Retrieves a Review object. : GET /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict()), 200
    abort(404)


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object: DELETE /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify(review.to_dict()), 200
    abort(404)


@app_views.route(
        '/places/<string:place_id>/reviews',
        methods=['POST'],
        strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review: POST /api/v1/places/<place_id>/reviews
    """
    place = storage.get(Place, place_id)
    if place is not None:
        try:
            json_data = request.get_json()
            if 'user_id' not in json_data:
                return jsonify({'error': 'Missing user_id'}), 400
            user = storage.get(User, json_data['user_id'])
            if user is not None:
                if 'text' not in json_data:
                    return jsonify({'error': 'Missing text'}), 400
                review = Review(**json_data)
                storage.new(review)
                storage.save()
                return jsonify(review.to_dict()), 201
            abort(404)
        except BadRequest:
            return jsonify({'error': 'Not a JSON'}), 400
    abort(404)


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object: PUT /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    banned_attributes = (
            'id',
            'user_id',
            'place_id',
            'created_at',
            'updated_at')
    if review is not None:
        try:
            json_data = request.get_json()
            for key, value in json_data.items():
                if key not in banned_attributes:
                    setattr(review, key, value)
            storage.save()
            return jsonify(review.to_dict()), 200
        except BadRequest:
            return jsonify({'error', 'Not a JSON'}), 400
    abort(404)
