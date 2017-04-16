from flask import json
from . import BaseTestCase
from copleyescalators.extensions import db
from copleyescalators.escalators.models import Escalator
from pprint import pprint


class EscalatorsTestCase(BaseTestCase):

    def setUp(self):
        super(TestTestCase, self).setUp()

        e = Escalator(top="top1", bottom="bottom1", up=True, down=False)
        db.session.add(e)
        e = Escalator(top="top2", bottom="bottom2", up=True, down=False)
        db.session.add(e)
        e = Escalator(top="top3", bottom="bottom3", up=True, down=False)
        db.session.add(e)
        e = Escalator(top="top4", bottom="bottom4", up=True, down=False)
        db.session.add(e)

        db.session.commit()

    def tearDown(self):
        Escalator.query.delete()
        db.session.commit()

    def test_get_all_escalators(self):
        esc = self.client.get('/escalators/')

        assert esc.status_code == 200
        assert len(esc.json) == 4
        assert len([e for e in esc.json if e["up"] is True]) == 4
        assert len([e for e in esc.json if e["down"] is False]) == 4
        assert len([e for e in esc.json if "top" in e["top"]]) == 4
        assert len([e for e in esc.json if "bottom" in e["bottom"]]) == 4

    def test_get_one_escalator(self):
        esc = self.client.get('/escalators/1')

        assert esc.status_code == 200
        assert esc.json is not None
        assert esc.json["id"] == 1
        assert esc.json["top"] == "top1"
        assert esc.json["bottom"] == "bottom1"
        assert esc.json["up"] is True
        assert esc.json["down"] is False

    def test_update_escalator(self):
        esc = self.client.post("/escalators/1/up",
                               data=json.dumps(dict(status="broken")),
                               content_type="application/json")

        assert esc.status_code == 200
        assert esc.json["escalator_updated"] is False

        esc = self.client.post("/escalators/1/up",
                               data=json.dumps(dict(status="broken")),
                               content_type="application/json")

        assert esc.status_code == 200
        assert esc.json["escalator_updated"] is True
