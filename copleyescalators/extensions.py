from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def date_string(dt=None):
    from datetime import datetime

    if dt is None:
        return datetime.today().strftime("%s")
    else:
        return dt.strftime("%s")
