"""Local configuration.

Note that Flask ignores attributes that aren't in ALL_CAPS, so do what
you want but Flask will only see the capitalized ones.
"""


from .base import BaseConfig
from ..project_root import path as project_root


class LocalConfig(BaseConfig):
    """Configuration for running in a local development environment.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s/data/escalators.db" % project_root
