#!/usr/bin/python3
"""
rest API module for reviews on all objects
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import *


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id=None):
    """
    method to display all reviews
    """
    if place_id is None:
        abort(404)
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    all_reviews = []
    for review in storage.all("Review").values():
        all_reviews.append(review.to_json())
    return jsonify(all_reviews)

@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def one_review(review_id=None):
    """
    method to get 1 review
    """
    if review_id is None:
        abort(404)
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_json())

@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """
    method to delete 1 review
    """
    if review_id is None:
        abort(404)
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return (jsonify({}), 200)

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                   strict_slashes=False)
def make_review(place_id=None):
    """
    method to create a review
    """
    if place_id is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    if "user_id" not in r.keys():
        abort(400, "Missing user_id")
    if "text" not in r.keys():
        abort(400, "Missing text")
    new = Reivew(r)
    storage.new(new)
    stroage.save()
    return (jsonify(storage.get("Review", new.id).to_json()), 201)

@app_views.route('/reviews/review_id', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id=None):
    """
    method to update a review
    """
    if review_id is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        abort(400, "Not a JSON")
    data = storage.get("Review", review_id)
    if data is None:
        abort(404)
    for key, value in r.items():
        if (key != "id" and key != "user_id" and key != "created_at"
            and key != "updated_at"):
            setattr(data, key, value)
    data.save()
    return (jsonify(data.to_json()), 200)
