#!/usr/bin/python3
"""
index Module
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


_classes = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User,
        }


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status"""
    return jsonify({'status': 'OK'}), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """stats"""
    d = {}
    for key, value in _classes.items():
        d[key] = storage.count(value)
    return jsonify(d), 200
