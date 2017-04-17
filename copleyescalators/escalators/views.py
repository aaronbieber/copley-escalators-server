from flask import Blueprint, jsonify, request
from .models import Escalator, EscalatorHistory
from copleyescalators.extensions import db, date_string
from pprint import pprint


escalators = Blueprint("escalators", __name__, url_prefix="/escalators")


@escalators.route('/', methods=["GET"])
def list_escalators():
    """List all escalators.
    """
    escalators = Escalator.query.all()

    return jsonify([e.to_dict() for e in escalators])


@escalators.route('/<int:id>')
def escalator(id):
    """Get one escalator.
    """
    escalator = Escalator.query.filter_by(id=id).first()

    if escalator is None:
        return jsonify(
            status=False,
            message="Escalator %s could not be found." % id
        ), 404

    return jsonify(escalator.to_dict())


@escalators.route('/<int:id>/<string:direction>', methods=["POST"])
def update_escalator(id, direction):
    """Update the status of one escalator.
    """

    if direction != "up" and direction != "down":
        return jsonify(error="Specify direction \"up\" or \"down\".")

    data = request.get_json(force=True)
    if "status" not in data or \
       data["status"] not in ["broken", "fixed"]:
        return jsonify(
            status=False,
            message="Provide a status key with value " +
            "\"broken\" or \"fixed\"."
        ), 400

    if "user" not in data or \
       len(data["user"]) == 0:
        return jsonify(
            status=False,
            message="You must provide a valid user UUID."
        ), 400

    if data["status"] == "broken":
        status_value = False
    else:
        status_value = True

    escalator = Escalator.query.filter_by(id=id).first()

    if escalator is None:
        return jsonify(
            status=False,
            message="Escalator %s (%s) could not be found." % (id, direction)
        ), 404

    return_value = {
        "status": True,
        "escalator_updated": False,
        "escalator": escalator.to_dict()
    }

    history = escalator.history[direction]
    last_updated = [h for h in history if h.user == data["user"]]
    if len(last_updated):
        if int(date_string()) - last_updated[0].added < (30 * 60 * 60):
            return jsonify(
                status=False,
                message=("Enhance your calm; you may not report the same " +
                         "escalator again within 30 minutes of your last " +
                         "report.")
            ), 429

    new_history = EscalatorHistory(escalator=id,
                                   user=data["user"],
                                   direction=direction,
                                   event=data["status"],
                                   added=date_string())
    db.session.add(new_history)

    if len(history) and history[0].event == new_history.event:
        if getattr(escalator, direction) != status_value:
            setattr(escalator, direction, status_value)
            return_value["escalator_updated"] = True

    try:
        db.session.commit()
    except:
        return jsonify(status=False)

    return jsonify(return_value)


@escalators.route('/<int:id>/history/<string:direction>')
def escalator_history(id, direction):
    """Get an escalator's history
    """

    if direction != "up" and direction != "down":
        return jsonify(error="Specify direction \"up\" or \"down\".")

    escalator = Escalator.query.filter_by(id=id).first()

    if escalator is None:
        return jsonify(
            status=False,
            message="Escalator %s could not be found." % id
        ), 404

    if direction == "up":
        return jsonify([h.to_dict() for h in escalator.history_up])

    if direction == "down":
        return jsonify([h.to_dict() for h in escalator.history_down])
