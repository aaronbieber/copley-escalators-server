from copleyescalators import app
from copleyescalators.escalators.models import Escalator, EscalatorHistory
from copleyescalators.users.models import User
from copleyescalators.extensions import db
from flask_script import Manager
import os

if "FLASK_CONFIG" not in os.environ:
    os.environ["FLASK_CONFIG"] = "copleyescalators.settings.local.LocalConfig"

app = app.create_app()
manager = Manager(app)


@manager.command
def init_db():
    if os.path.isfile("copleyescalators/data/escalators.db"):
        print("Found existing database file; deleting...")
        os.remove("copleyescalators/data/escalators.db")

    print("Initializing database in \"%s\"" %
          app.config["SQLALCHEMY_DATABASE_URI"])
    write_schema()
    write_seed_data()


def write_schema():
    print("Creating schema...")
    db.create_all()


def write_seed_data():
    print("Writing seed data...")
    escalators = [
        {"top":    "Westin Hotel",
         "bottom": "Dartmouth St"},
        {"top":    "Au Bon Pain",
         "bottom": "Dartmouth St"},
        {"top":    "Louis Vuitton",
         "bottom": "Au Bon Pain"},
        {"top":    "Currency Exchange",
         "bottom": "Sur La Table"},
        {"top":    "Skylobby",
         "bottom": "Legal Sea Foods"},
        {"top":    "Tiffany's",
         "bottom": "Champions"},
        {"top":    "Victoria's Secret",
         "bottom": "Tiffany's"},
        {"top":    "Champions",
         "bottom": "Huntington Ave"}
    ]

    for escalator in escalators:
        model = Escalator(top=escalator["top"],
                          bottom=escalator["bottom"],
                          up=True,
                          down=True)
        print(model)
        db.session.add(model)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
