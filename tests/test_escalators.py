from flask import json
from . import BaseTestCase
from datetime import datetime
from copleyescalators.extensions import db, date_string
from copleyescalators.escalators.models import Escalator, EscalatorHistory
from copleyescalators.users.models import Auth
from pprint import pprint


class EscalatorsReadTestCase(BaseTestCase):

    def setUp(self):
        super(EscalatorsReadTestCase, self).setUp()

        e = Escalator(top="top1", bottom="bottom1", up=True, down=False)
        db.session.add(e)
        e = Escalator(top="top2", bottom="bottom2", up=True, down=False)
        db.session.add(e)
        e = Escalator(top="top3", bottom="bottom3", up=True, down=False)
        db.session.add(e)
        e = Escalator(top="top4", bottom="bottom4", up=True, down=False)
        db.session.add(e)

        h = EscalatorHistory(escalator=1,
                             direction="up",
                             event="broken",
                             added=date_string(
                                 datetime(2017, 1, 1, 7, 0, 0)))
        db.session.add(h)

        h = EscalatorHistory(escalator=1,
                             direction="up",
                             event="broken",
                             added=date_string(
                                 datetime(2017, 1, 1, 7, 30, 0)))
        db.session.add(h)

        h = EscalatorHistory(escalator=1,
                             direction="up",
                             event="fixed",
                             added=date_string(
                                 datetime(2017, 1, 1, 8, 00, 0)))
        db.session.add(h)

        a = Auth(token="token-string")
        db.session.add(a)

        db.session.commit()

    def tearDown(self):
        super(EscalatorsReadTestCase, self).tearDown()

    def test_get_all_escalators(self):
        esc = self.client.get("/escalators/",
                              headers={"Auth-Token": "token-string"})

        assert esc.status_code == 200
        assert len(esc.json) == 4
        assert len([e for e in esc.json if e["up"] is True]) == 4
        assert len([e for e in esc.json if e["down"] is False]) == 4
        assert len([e for e in esc.json if "top" in e["top"]]) == 4
        assert len([e for e in esc.json if "bottom" in e["bottom"]]) == 4

    def test_get_one_escalator(self):
        esc = self.client.get("/escalators/1",
                              headers={"Auth-Token": "token-string"})

        assert esc.status_code == 200
        assert esc.json is not None
        assert esc.json["id"] == 1
        assert esc.json["top"] == "top1"
        assert esc.json["bottom"] == "bottom1"
        assert esc.json["up"] is True
        assert esc.json["down"] is False

    def test_get_one_nonexistent_escalator(self):
        esc = self.client.get("/escalators/999",
                              headers={"Auth-Token": "token-string"})

        assert esc.status_code == 404
        assert "status" in esc.json
        assert esc.json["status"] is False

    def test_get_escalator_history(self):
        esch = self.client.get("/escalators/1/history/up",
                              headers={"Auth-Token": "token-string"})

        assert esch.status_code == 200
        assert len(esch.json) == 3
        assert len([h for h in esch.json if h["direction"] == "up"]) == 3

        # Ensures descending order by time
        assert esch.json[0]["event"] == "fixed"
        assert esch.json[1]["event"] == "broken"
        assert esch.json[2]["event"] == "broken"

    def test_get_nonexistent_escalator_hisotry(self):
        esch = self.client.get("/escalators/999/history/up",
                               headers={"Auth-Token": "token-string"})

        assert esch.status_code == 404
        assert "status" in esch.json
        assert esch.json["status"] is False


class EscalatorsUpdateTestCase(BaseTestCase):

    def setUp(self):
        super(EscalatorsUpdateTestCase, self).setUp()

        e = Escalator(top="top1", bottom="bottom1", up=True, down=False)
        db.session.add(e)
        e = Escalator(top="top2", bottom="bottom2", up=True, down=False)
        db.session.add(e)

        a = Auth(token="token-string")
        db.session.add(a)

        db.session.commit()

    def tearDown(self):
        super(EscalatorsUpdateTestCase, self).tearDown()

    def test_invalid_status(self):
        esc = self.client.post("/escalators/1/up",
                               data=json.dumps(dict(
                                   user="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                                   status="quux")),
                               content_type="application/json",
                               headers={"Auth-Token": "token-string"})

        assert esc.status_code == 400
        assert "message" in esc.json
        assert "status" in esc.json["message"]

    def test_update_with_missing_user(self):
        esc = self.client.post("/escalators/1/up",
                               data=json.dumps(dict(status="broken")),
                               content_type="application/json",
                               headers={"Auth-Token": "token-string"})

        assert esc.status_code == 400
        assert "message" in esc.json
        assert "user" in esc.json["message"]

    def test_update_escalator(self):
        esc = self.client.post("/escalators/1/up",
                               data=json.dumps(dict(
                                   user="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                                   status="broken")),
                               content_type="application/json",
                               headers={"Auth-Token": "token-string"})

        assert esc.status_code == 200
        assert esc.json["escalator_updated"] is False

        esc = self.client.post("/escalators/1/up",
                               data=json.dumps(dict(
                                   user="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                                   status="broken")),
                               content_type="application/json",
                               headers={"Auth-Token": "token-string"})

        assert esc.status_code == 200
        assert esc.json["escalator_updated"] is True

    def test_update_escalator_too_quickly(self):
        now = int(datetime.today().strftime("%s"))
        added = now - 1790

        esc = self.client.post("/escalators/2/up",
                               data=json.dumps(dict(
                                   user="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                                   status="broken",
                                   added=added)),
                               content_type="application/json",
                               headers={"Auth-Token": "token-string"})

        assert esc.status_code == 200
        assert esc.json["status"] is True

        esc = self.client.post("/escalators/2/up",
                               data=json.dumps(dict(
                                   user="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                                   status="broken")),
                               content_type="application/json",
                               headers={"Auth-Token": "token-string"})

        assert esc.status_code == 429
        assert esc.json["status"] is False

    def test_update_nonexistent_escalator(self):
        esc = self.client.post("/escalators/999/up",
                               data=json.dumps(dict(
                                   user="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                                   status="broken")),
                               content_type="application/json",
                               headers={"Auth-Token": "token-string"})

        assert esc.status_code == 404
        assert "status" in esc.json
        assert esc.json["status"] is False
