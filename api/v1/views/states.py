#!/usr/bin/python3
"""
rest API for all State objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import State, storage


@app_views.route('/states/', methods=['GET'],
                 strict_slashes=False)
def all_states():
    """
    method to list all states
    """
    all_states = {}
    for state in storage.all("State").values():
        all_states.append(state.to_json())
    return jsonify(all_states)

@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def one_state(state_id=None):
    """
    method to get 1 state
    """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """
    method to delete 1 state
    """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({})

@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def make_state():
    """
    method to create 1 state
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    if "name" not in r.keys():
        abort(400, "Missing name")
    new = State(r)
    storage.new(new)
    storage.save()
    return (jsonify(storage.get("State", new.id).to_json()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id=None):
    """
    method to update 1 state
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    data = storage.get("State", state_id)
    if data is None:
        abort(404)
    for key, value in r.items():
        if key != "id" and key != "created_at" and key != "updated_at":
           setattr(data, key, value)
    data.save()
    return (jsonify(data.to_json()), 200)
