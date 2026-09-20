def get_token(client, username="testadmin", password="testpass123", role="admin"):
    client.post("/api/users", json={"username": username, "password": password, "role": role})
    response = client.post("/api/login", data={"username": username, "password": password})
    return response.json()["access_token"]


def test_create_asset(client):
    token = get_token(client)
    response = client.post(
        "/api/assets",
        json={"asset_number": "AST-001", "asset_type": "Laptop", "name": "Dell Latitude", "status": "active"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["asset_number"] == "AST-001"


def test_get_assets(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/assets", json={"asset_number": "AST-001", "asset_type": "Laptop", "name": "Dell"}, headers=headers)

    response = client.get("/api/assets", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_asset(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = client.post("/api/assets", json={"asset_number": "AST-001", "asset_type": "Laptop", "name": "Dell"}, headers=headers)
    asset_id = create_res.json()["id"]

    update_res = client.put(f"/api/assets/{asset_id}", json={
        "asset_number": "AST-001", "asset_type": "Laptop", "name": "Dell", "status": "maintenance"
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "maintenance"


def test_delete_asset(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = client.post("/api/assets", json={"asset_number": "AST-001", "asset_type": "Laptop", "name": "Dell"}, headers=headers)
    asset_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/assets/{asset_id}", headers=headers)
    assert delete_res.status_code == 200

    get_res = client.get("/api/assets", headers=headers)
    assert len(get_res.json()) == 0