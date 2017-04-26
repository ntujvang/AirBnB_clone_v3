#!/usr/bin/python3
"""
rest API for all Place-Amenity links
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import Amenity, Place, storage
from os import getenv
from sqlalchemy import inspect


if getenv("HBNB_TYPE_STORAGE") != "db":

else:

