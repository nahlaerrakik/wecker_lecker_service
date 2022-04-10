def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

    result = response.json()
    assert result == "Wecker Lecker Service"
