#!/usr/bin/python3
"""
rest API for all user objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import User, storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_user():
    """
    method to list all user
    """
    all_user = {}
    for user in storage.all("User").values():
        all_user.append(user.to_json())
    return jsonify(all_user)

@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def one_user(user_id=None):
    """
    method to list 1 user
    """
    if user_id is None:
        abort(404)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """
    method to delete 1 user
    """
    if user_id is None:
        abort(404)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({})

@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def make_user():
    """
    create 1 user
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    if 'email' not in r.keys():
        abort(400, "Missing email")
    if 'password' not in r.keys():
        abort(400, "Missing password")
    new = User(r)
    storage.new(new)
    storage.save()
    return (jsonify(storage.get("User", new.id).to_json()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id=None):
    """
    update a user
    """
    if user_id is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    data = storage.get("User", user_id)
    if data is None:
        abort(404)
    for key, value in r.items():
        if (key != "id" and key != "email" and key != "created_at"
            and key != "updated_at"):
            setattr(data, key, value)
    data.save()
    return (jsonify(data.to_json()), 200)
