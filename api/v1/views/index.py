#!/usr/bin/python3
"""
API index
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    method that displays status
    """
    return (jsonify({"status": "OK"}))

@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    method that displays object count
    """
    models = {"amenities": "Amenity", "cities": "City", "places": "Place",
            "reviews": "Review", "states": "State", "users": "User"}
    temp_dict = {}
    for key in models.keys():
        temp_dict[key] = storage.count(key)
    return jsonify(temp_dict)
