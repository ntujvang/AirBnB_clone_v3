#!/usr/bin/python3
"""
rest API module for all City objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import City, State, storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id=None):
    """
    method to get all cities
    """
    all_cities = {}
    if state_id is None:
        abort(404)
    for city in storage.all("City").values():
        all_cities = city.to_json()
    return jsonify(all_cities)

@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def one_city(city_id=None):
    """
    method to get one city
    """
    if city_id is None:
        abort(404)
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())

@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """
    method to delete a city
    """
    if city_id is None:
        abort(404)
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({})

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def make_city(state_id=None):
    """
    method to make a city
    """
    if state_id is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    if 'name' not in r.keys():
        abort(400, "Missing name")
    new = City(r)
    storage.new(new)
    storage.save()
    return (jsonify(storage.get("City", new.id).to_json()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id=None):
    """
    method to update a ciy
    """
    if city_id is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    data = storage.get("City", city_id)
    if data is None:
        abort(404)
    for key, value in r.items():
        if (key != "id" and key != "created_at" and key != "state_id"
            and key != "updated_at"):
            setattr(data, key, value)
    data.save()
    return (jsonify(data.to_json()), 200)
