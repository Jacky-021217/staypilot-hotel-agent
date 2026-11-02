"""Run: cd project_root && python -m pytest -q"""
import os
import sys
from pathlib import Path

os.environ.setdefault("STAYPILOT_API_KEY", "test-only-secret-key")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

import pytest
from fastapi.testclient import TestClient
import app as api

API_KEY = "test-only-secret-key"

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(api, "DB_PATH", tmp_path / "tests.sqlite3")
    monkeypatch.setattr(api, "API_KEY", API_KEY)
    with TestClient(api.app) as c:
        yield c


def payload(request_id="test-one", confirmed=True):
    return {
        "request_id": request_id,
        "room_number": "1208",
        "category": "maintenance",
        "summary": "空调不能制冷",
        "quantity": 1,
        "priority": "normal",
        "confirmed": confirmed,
    }


def auth():
    return {"X-API-Key": API_KEY}


def test_health(client):
    assert client.get("/health").json() == {"ok": True, "demo": True}


def test_api_key_required(client):
    assert client.post("/tickets", json=payload()).status_code == 401
    assert client.post("/tickets", headers={"X-API-Key": "wrong"}, json=payload()).status_code == 401


def test_confirmation_required(client):
    r = client.post("/tickets", headers=auth(), json=payload(confirmed=False))
    assert r.status_code == 400
    assert client.get("/tickets", headers=auth()).json()["count"] == 0


def test_create_query_and_duplicate_id(client):
    first = client.post("/tickets", headers=auth(), json=payload())
    assert first.status_code == 201, first.text
    ticket = first.json()
    assert ticket["ticket_id"].startswith("WO-")
    assert ticket["department"] == "engineering"
    repeat = client.post("/tickets", headers=auth(), json=payload())
    assert repeat.status_code == 201
    assert repeat.json()["ticket_id"] == ticket["ticket_id"]
    assert client.get("/tickets", headers=auth()).json()["count"] == 1
    assert client.get(f'/tickets/{ticket["ticket_id"]}', headers=auth()).json()["status"] == "open"


def test_wrong_fields_rejected(client):
    wrong = payload()
    wrong["room_number"] = "?"
    assert client.post("/tickets", headers=auth(), json=wrong).status_code == 422
    wrong = payload()
    wrong["quantity"] = 100
    assert client.post("/tickets", headers=auth(), json=wrong).status_code == 422


def test_state_machine(client):
    tid = client.post("/tickets", headers=auth(), json=payload()).json()["ticket_id"]
    for status in ["accepted", "in_progress", "completed"]:
        r = client.patch(f"/tickets/{tid}", headers=auth(), json={"status": status})
        assert r.status_code == 200, r.text
        assert r.json()["status"] == status
    r = client.patch(f"/tickets/{tid}", headers=auth(), json={"status": "cancelled"})
    assert r.status_code == 409


def test_not_found(client):
    assert client.get("/tickets/WO-UNKNOWN", headers=auth()).status_code == 404
