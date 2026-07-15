def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_correct_fields(client):
    data = client.get("/health").json()
    assert data["status"] == "ok"
    assert data["app"] == "AEGIS"
    assert "version" in data
    assert "env" in data
