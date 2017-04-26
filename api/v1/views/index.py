#!/usr/bin/python3
"""
API index
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    return (jsonify({"status": "OK"}))

@app_views.route('/stats')
def stats():
    models = {"amenities": "Amenity", "cities": "City", "places": "Place",
            "reviews": "Review", "states": "State", "users": "User"}
    temp_dict = {}
    for key, value in mondels.items():
        temp_dict[k] = storage.count(value)
    return jsonify(temp_dict)
