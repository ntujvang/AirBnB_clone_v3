#!/usr/bin/python3
"""
rest API module for reviews on all objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import *


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id=None):
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    all_reviews = []
    for review in storage.all("Review").values():
        all_reviews.append(review.to_json())
    return jsonify(all_reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'])
def one_review(review_id=None):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_json())

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id=None):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return (jsonify({}), 200)

@app_reviews.route('/places/<place_id>/reviews', methods=['POST'])
def make_review(place_id=None):
    try:
        r = request.get_json()
    except:
        abort(400, "Not a JSON")
    if "user_id" not in r.keys():
        abort(400, "Missing user_id")
    if "text" not in data:
        abort(400, "Missing text")
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    user = storage.get("User", r.get("user_id"))
    if user is None:
        abort(404)
    r["review_id"] = review_id
    new = Reivew(r)
    storage.new(new)
    stroage.save()
    return (jsonify(storage.get("Review", new.id).to_json()), 201)

@app_views.route('/reviews/review_id', methods=['PUT'])
def update_review(review_id=None):
    try:
        r = request.get_json()
    except:
        abort(400, "Not a JSON")
    data = storage.get("Review", review_id)
    if data is None:
        abort(404)
    for key, value in r.items():
        if (key != "id" and key != "user_id" and key != "created_at"
            and key != "updated_at"):
            setattr(data, key, value)
    data.save()
    return (jsonify(data.to_json(), 200)
