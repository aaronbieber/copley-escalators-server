from flask import Blueprint, Response


home = Blueprint('', __name__)


@home.route('/')
def index():
    return Response("Hello, world.")
