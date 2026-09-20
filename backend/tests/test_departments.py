def get_token(client, username="testadmin", password="testpass123", role="admin"):
    client.post("/api/users", json={"username": username, "password": password, "role": role})
    response = client.post("/api/login", data={"username": username, "password": password})
    return response.json()["access_token"]


def test_create_department(client):
    token = get_token(client)
    response = client.post(
        "/api/departments",
        json={"name": "IT", "manager": "Yuki Tanaka"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "IT"
    assert "id" in data


def test_get_departments(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/departments", json={"name": "IT", "manager": "Yuki"}, headers=headers)

    response = client.get("/api/departments", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_department(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = client.post("/api/departments", json={"name": "IT", "manager": "Yuki"}, headers=headers)
    dept_id = create_res.json()["id"]

    update_res = client.put(f"/api/departments/{dept_id}", json={"name": "IT Support", "manager": "Yuki"}, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "IT Support"


def test_delete_department(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = client.post("/api/departments", json={"name": "IT", "manager": "Yuki"}, headers=headers)
    dept_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/departments/{dept_id}", headers=headers)
    assert delete_res.status_code == 200

    get_res = client.get("/api/departments", headers=headers)
    assert len(get_res.json()) == 0


def test_update_nonexistent_department(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put("/api/departments/999", json={"name": "Ghost", "manager": "Nobody"}, headers=headers)
    assert response.status_code == 404