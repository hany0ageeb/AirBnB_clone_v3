#!/usr/bin/python3
"""
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(x):
    """handle @app.teardown_appcontext that calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(x):
    """
    a handler for 404 errors that returns a JSON-formatted
    404 status code response"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    from os import getenv
    app.run(
            host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True)
