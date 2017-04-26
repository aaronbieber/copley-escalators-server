"""A before-request function that will verify whether the request
should be permitted to continue. Not strictly user auth in this case,
but, close enough.
"""
from flask import request, jsonify
from .models import Auth


def auth():
    if "Auth-Token" in request.headers:
        tokens = [a.token for a in Auth.query.all()]

        if request.headers["Auth-Token"] in tokens:
            return None

    return jsonify(
        status=False,
        message="Access denied."
    ), 401
