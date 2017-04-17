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
        primaryjoin="and_(Escalator.id==EscalatorHistory.escalator,"
        "EscalatorHistory.direction=='up')",
        order_by=db.desc("added"))

    history_down = db.relationship(
        'EscalatorHistory',
        primaryjoin="and_(Escalator.id==EscalatorHistory.escalator,"
        "EscalatorHistory.direction=='down')",
        order_by=db.desc("added"))

    @property
    def history(self):
        return {
            "up": self.history_up,
            "down": self.history_down
        }

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()
                if k != "_sa_instance_state"}

    def __repr__(self):
        return (
            ("Escalator(id={self.id}, top={self.top}, bottom={self.bottom}, " +
             "up={self.up}, down={self.down})")
            .format(self=self))


class EscalatorHistory(db.Model):
    """Escalator history model.
    """
    __tablename__ = "escalator_history"

    id = db.Column("id", db.Integer, primary_key=True)
    escalator = db.Column("escalator",
                          db.Integer,
                          db.ForeignKey("escalators.id"))
    user = db.Column("user",
                     db.String(40))
    direction = db.Column("direction", db.String(4), nullable=False)
    event = db.Column("event", db.String(25), nullable=False)
    added = db.Column("added", db.Integer, nullable=False)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()
                if k != "_sa_instance_state"}

    def __repr__(self):
        return (
            ("EscalatorHistory(id={self.id}, direction={self.direction}, " +
             "event={self.event}, user={self.user} added={self.added})")
            .format(self=self))
