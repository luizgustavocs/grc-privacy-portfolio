from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def future(days: int = 1) -> str:
    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()


def test_health_has_security_headers():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "default-src 'none'" in response.headers["Content-Security-Policy"]


def test_create_and_read_appointment():
    created = client.post("/appointments", json={"patient_ref": "P-000123", "clinic_id": 7, "starts_at": future()})
    assert created.status_code == 201
    fetched = client.get(f"/appointments/{created.json()['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["patient_ref"] == "P-000123"


def test_rejects_identifiable_patient_reference():
    # A CPF or a name must not be accepted where a pseudonymised reference is expected
    response = client.post("/appointments", json={"patient_ref": "123.456.789-00", "clinic_id": 7, "starts_at": future()})
    assert response.status_code == 422


def test_rejects_past_appointment():
    response = client.post("/appointments", json={"patient_ref": "P-000123", "clinic_id": 7, "starts_at": future(-1)})
    assert response.status_code == 422


def test_unknown_appointment_returns_404():
    assert client.get("/appointments/00000000-0000-0000-0000-000000000000").status_code == 404


def test_api_docs_are_disabled():
    assert client.get("/docs").status_code == 404
