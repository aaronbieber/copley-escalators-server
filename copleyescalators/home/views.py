from flask import Blueprint, Response, jsonify
from .models import User


home = Blueprint('home', __name__)


@home.route('/users')
def users():
    users = User.query.all()
    return jsonify(users=[u.to_dict() for u in users])


@home.route('/')
def index():
    return Response("Hello, world.")
