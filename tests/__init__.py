from flask_testing import TestCase
from copleyescalators import create_app
from copleyescalators.extensions import db


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.client = self.app.test_client()
        db.create_all()

    def create_app(self):
        return create_app()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
