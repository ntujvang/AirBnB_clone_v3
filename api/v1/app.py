#!/usr/bin/python3
"""
Initiates a rest API
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def storage_close(exception):
    """
    method to close storage
    """
    storage.close()

@app.errorhandler(404)
def not_found(e):
    """
    method for 404 handling
    """
    return (jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
