from flask import Blueprint, jsonify, request
from .models import Escalator, EscalatorHistory
from copleyescalators.extensions import db, date_string


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

    # escalator = Escalator.query.filter_by(id=id).first()
    history = EscalatorHistory.query.filter_by(
        escalator=id,
        direction=direction
    ).order_by(db.desc(EscalatorHistory.added)).all()

    new_history = EscalatorHistory(escalator=id,
                                   direction=direction,
                                   event=data["status"],
                                   added=date_string())
    db.session.add(new_history)

    if len(history) and history[0].event == new_history.event:
        escalator = Escalator.query.filter_by(id=id).first()
        setattr(escalator, direction, not getattr(escalator, direction))

    try:
        db.session.commit()
    except:
        return jsonify({"status": "Error"})

    return jsonify({"status": "OK"})


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
