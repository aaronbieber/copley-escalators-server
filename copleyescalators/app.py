"""Initialize the Flask app and bootstrap all modules and interfaces."""

import os
from flask import Flask, url_for
from pprint import pprint
from .extensions import db
from .home import home

BLUEPRINTS = [
    home
]

# For import *
__all__ = ['create_app']


def list_routes(app):
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        pprint(rule)


def create_app():
    """Build the WSGI application callable."""
    app = Flask(__name__)
    app.debug = True
    configure_app(app)
    configure_blueprints(app, BLUEPRINTS)
    db.init_app(app)

    list_routes(app)

    return app


def configure_app(app):
    """Load a Flask application configuration.
    """
    if 'FLASK_CONFIG' in os.environ:
        app.config.from_object(os.environ['FLASK_CONFIG'])
    else:
        raise ValueError("Cannot load configuration without a FLASK_CONFIG variable.")


def configure_blueprints(app, blueprints):
    """Register the given blueprints with the app."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


if __name__ == '__main__':
    """Manually run the WSGI application.

This should probably NOT be used; instead, run a local server through
the uwsgi program using the included shell script (see "bin").
"""
    create_app().run()
