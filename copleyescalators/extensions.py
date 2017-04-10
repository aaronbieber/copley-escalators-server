from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def date_string(dt=None):
    from datetime import datetime

    if dt is None:
        return datetime.today().strftime("%Y-%m-%d %H:%M:%S.000")
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S.000")
