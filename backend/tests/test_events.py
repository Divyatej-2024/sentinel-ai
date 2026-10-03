from pydantic import SecretStr

from app.core.config import settings


def payload(**overrides):
    event = {
        "timestamp": "2026-10-03T12:00:00Z",
        "event_type": "authentication",
        "source": "windows",
        "source_ip": "192.168.1.50",
        "username": "administrator",
        "hostname": "WORKSTATION-01",
        "action": "login",
        "status": "failed",
        "severity": "high",
        "metadata": {"logon_type": 3},
    }
    return event | overrides


def test_create_get_and_documentation(client):
    response = client.post("/api/v1/events", json=payload())
    assert response.status_code == 201
    created = response.json()
    assert created["metadata"] == {"logon_type": 3}
    assert created["source_ip"] == "192.168.1.50"
    assert client.get(f"/api/v1/events/{created['event_id']}").json() == created
    assert client.get("/api/docs").status_code == 200
    assert client.get("/api/redoc").status_code == 200


def test_list_filters_and_pagination(client):
    client.post("/api/v1/events", json=payload())
    client.post(
        "/api/v1/events",
        json=payload(username="other", source_ip="10.0.0.2", severity="low"),
    )
    response = client.get(
        "/api/v1/events",
        params={"username": "administrator", "severity": "high", "limit": 1, "offset": 0},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "administrator"
    assert client.get("/api/v1/events", params={"offset": 2}).json() == []


def test_reject_invalid_input_and_query(client):
    assert client.post("/api/v1/events", json=payload(source_ip="not-an-ip")).status_code == 422
    assert client.post("/api/v1/events", json=payload(untrusted_field="ignored")).status_code == 422
    assert client.get("/api/v1/events", params={"limit": 201}).status_code == 422
    assert client.get("/api/v1/events", params={"severity": "urgent"}).status_code == 422
    assert client.get("/api/v1/events", params={"source_ip": "not-an-ip"}).status_code == 422


def test_missing_event(client):
    from uuid import uuid4

    assert client.get(f"/api/v1/events/{uuid4()}").status_code == 404


def test_configured_api_key_protects_event_routes(client, monkeypatch):
    monkeypatch.setattr(settings, "api_key", SecretStr("test-ingestion-key"))
    assert client.get("/api/v1/events").status_code == 401
    headers = {"X-API-Key": "test-ingestion-key"}
    assert client.get("/api/v1/events", headers=headers).status_code == 200
    assert client.post("/api/v1/events", json=payload(), headers=headers).status_code == 201


def test_postgres_url_selects_psycopg_driver():
    from app.core.config import Settings

    assert (
        Settings(database_url="postgresql://user:pass@host/db").database_url
        == "postgresql+psycopg://user:pass@host/db"
    )


def test_time_filters_validate_order_and_timezone(client):
    client.post("/api/v1/events", json=payload())
    result = client.get(
        "/api/v1/events",
        params={
            "start_time": "2026-10-03T11:59:00Z",
            "end_time": "2026-10-03T12:01:00Z",
        },
    )
    assert len(result.json()) == 1
    reversed_range = client.get(
        "/api/v1/events",
        params={
            "start_time": "2026-10-04T00:00:00Z",
            "end_time": "2026-10-03T00:00:00Z",
        },
    )
    assert reversed_range.status_code == 422
