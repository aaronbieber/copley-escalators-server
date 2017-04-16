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
        return jsonify(error="Escalator %s not found." % id)

    return jsonify(escalator.to_dict())


@escalators.route('/<int:id>/<string:direction>', methods=["POST"])
def update_escalator(id, direction):
    """Update the status of one escalator.
    """
    if direction != "up" and direction != "down":
        return jsonify(error="Specify direction \"up\" or \"down\".")

    data = request.get_json(force=True)
    if "status" not in data or \
       data["status"] != "broken" and data["status"] != "fixed":
        return jsonify(error="Provide a status key with value " +
                       "\"broken\" or \"fixed\".")

    if data["status"] == "broken":
        status_value = False
    else:
        status_value = True

    escalator = Escalator.query.filter_by(id=id).first()
    history = escalator.history[direction]

    new_history = EscalatorHistory(escalator=id,
                                   direction=direction,
                                   event=data["status"],
                                   added=date_string())
    db.session.add(new_history)

    escalator_updated = False
    if len(history) and history[0].event == new_history.event:
        if getattr(escalator, direction) != status_value:
            setattr(escalator, direction, status_value)
            escalator_updated = True

    try:
        db.session.commit()
    except:
        return jsonify(status="Error")

    return jsonify(
        new_history=new_history.to_dict(),
        escalator=escalator.to_dict(),
        escalator_updated=escalator_updated
    )


@escalators.route('/<int:id>/history/<string:direction>')
def escalator_history(id, direction):
    """Get an escalator's history
    """
    if direction != "up" and direction != "down":
        return jsonify(error="Specify direction \"up\" or \"down\".")

    escalator = Escalator.query.filter_by(id=id).first()

    if escalator is None:
        return jsonify(error="Escalator %s not found." % id)

    if direction == "up":
        return jsonify([h.to_dict() for h in escalator.history_up])

    if direction == "down":
        return jsonify([h.to_dict() for h in escalator.history_down])
