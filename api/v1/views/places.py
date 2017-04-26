#!/usr/bin/python3
"""
rest API for all places objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import State, storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def list_places(city_id=None):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    all_places = []
    for place in storage.all("Place").values():
        all_places.append(place.to_json())
    return jsonify(all_places)

@app_views.route('/places/<place_id>', methods=['GET'])
def one_place(place_id=None):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_json())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id=None):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    stoage.delete(place)
    return (jsonify({}), 200)

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def make_place(city_id=None):
    try:
        r = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "name" not in r.keys():
        abort(400, "Missing name")
    if "user_id" not in r.keys():
        abort(400, "Missing user_id")
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    user = storage.get("User", r.get("user_id"))
    if user is None:
        abort(404)
    r["city_id"] = city_id
    new = Place(r)
    storage.new(new)
    storage.save()
    return (jsonify(storage.get("Place", new.id).to_json()), 201)

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id=None):
    try:
        r = request.get_json()
    except:
        abort(400, "Not a JSON")
    data = storage.get("Place", place_id)
    if data is None:
        abort(404)
    for key, value in r.items():
        if (key != "id" and key != "user_id" and key != "city_id"
            key != "created_at" and key != "updated_at"):
            setattr(data, key, value)
    data.save()
    return (jsonify(data.to_json(), 200)
