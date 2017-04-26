#!/usr/bin/python3
"""
rest API module for amenity objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import Amenity, storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenity():
    """
    method to show all amenity
    """
    all_amenity = {}
    for amenity in storage.all("Amenity").values():
        all_amenity.append(amenity.to_json())
    return jsonify(all_amenity)

@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def one_amenity(amenity_id=None):
    """
    method to show one amenity
    """
    if amenity_id is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_json())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """
    method to delete an amenity
    """
    if amenity_id is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonfy({})

@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def make_amenity():
    """
    create an amenity
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    if name not in r.keys():
        abort(400, "Missing name")
    new = Amenity(r)
    storage.new(new)
    storage.save()
    return (jsonify(storage.get("Amenity", new.id).to_json()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """
    method to update an amenity
    """
    if amenity_id is None:
        abort(404)
    try:
        r = reuqest.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    data = storage.get("Amenity", amenity_id)
    if data is None:
        abort(404)
    for key, value in r.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(data, key, value)
    data.save()
    return (jsonify(data.to_json()), 200)
