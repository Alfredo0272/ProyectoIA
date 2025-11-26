from src.db.mongo import get_db
from pymongo.errors import PyMongoError
import pytest

def fake_client_error(*args, **kwargs):
    raise PyMongoError("Fallo simulado")

def test_connection_failure(monkeypatch):
    monkeypatch.setattr("src.db.mongo.MongoClient", fake_client_error)
    with pytest.raises(PyMongoError):
        get_db()


def test_successful_connection(monkeypatch):
    class FakeDB:
        def command(self, cmd):
            if cmd == "ping":
                return {"ok": 1}

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        def __getitem__(self, name):
            return FakeDB()

    monkeypatch.setattr("src.db.mongo.MongoClient", FakeClient)

    db = get_db()
    result = db.command("ping")

    assert result["ok"] == 1
