"""SQLAlchemy model definitions.
"""


from copleyescalators.extensions import db


class User(db.Model):
    """User model.
    """
    __tablename__ = "users"

    id = db.Column("id", db.String(40), primary_key=True)
    name = db.Column("name", db.String(100), nullable=True)

    def __unicode__(self):
        """Stringify.
        """
        return u"<User %s>" % self.name

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()
                if k != "_sa_instance_state"}
