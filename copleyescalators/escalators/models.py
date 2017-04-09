"""SQLAlchemy model definitions.
"""


from copleyescalators.extensions import db


class Escalator(db.Model):
    """Escalator model.
    """
    __tablename__ = "escalators"

    id = db.Column("id", db.Integer, primary_key=True)
    top = db.Column("top", db.String(100), nullable=False)
    bottom = db.Column("bottom", db.String(100), nullable=False)
    up = db.Column("up", db.Boolean, nullable=False)
    down = db.Column("down", db.Boolean, nullable=False)

    history_up = db.relationship(
        'EscalatorHistory',
        lazy='joined',
        primaryjoin="and_(Escalator.id==EscalatorHistory.escalator,"
        "EscalatorHistory.direction=='up')")

    history_down = db.relationship(
        'EscalatorHistory',
        lazy='joined',
        primaryjoin="and_(Escalator.id==EscalatorHistory.escalator,"
        "EscalatorHistory.direction=='down')")

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()
                if k != "_sa_instance_state"}


class EscalatorHistory(db.Model):
    """Escalator history model.
    """
    __tablename__ = "escalator_history"

    id = db.Column("id", db.Integer, primary_key=True)
    escalator = db.Column("escalator",
                          db.Integer,
                          db.ForeignKey("escalators.id"))
    direction = db.Column("direction", db.String(4), nullable=False)
    event = db.Column("event", db.String(25), nullable=False)
    added = db.Column("added", db.String(25), nullable=False)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()
                if k != "_sa_instance_state"}
