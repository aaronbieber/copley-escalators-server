"""SQLAlchemy model definitions.
"""


from copleyescalators.extensions import db


class User(db.Model):
    """User model.
    """
    __tablename__ = "users"

    id = db.Column("id", db.String(40), primary_key=True)
    name = db.Column("name", db.String(100), nullable=True)

    def __repr__(self):
        """Debug representation.
        """
        return u"<User id={user.id}, name={user.name}>".format(user=self)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()
                if k != "_sa_instance_state"}


class Auth(db.Model):
    """Auth tokens model.
    """
    __tablename__ = "auth_tokens"

    token = db.Column("token", db.String(40), primary_key=True)

    def __unicode__(self):
        """Stringify.
        """
        return u"<Token token=%s>" % self.token

    def tokens_as_list(self):
        return [r.token for r in self.query.all()]
