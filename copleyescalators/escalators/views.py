from flask import Blueprint, Response, jsonify
from .models import Escalator
from pprint import pprint


escalators = Blueprint("escalators", __name__, url_prefix="/escalators")


@escalators.route('/', methods=["GET"])
def list_escalators():
    """List all escalators.
    """
    escalators = Escalator.query.all()

    data = []
    for escalator in escalators:
        item = escalator.to_dict()
        item["history"] = {
            "up": [h.to_dict() for h in escalator.history_up],
            "down": [h.to_dict() for h in escalator.history_down]
        }
        del item['history_down']
        del item['history_up']
        data.append(item)

    return jsonify(data)
