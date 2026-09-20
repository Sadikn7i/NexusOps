def get_token(client, username="testadmin", password="testpass123", role="admin"):
    client.post("/api/users", json={"username": username, "password": password, "role": role})
    response = client.post("/api/login", data={"username": username, "password": password})
    return response.json()["access_token"]


def test_create_machine(client):
    token = get_token(client)
    response = client.post(
        "/api/machines",
        json={"machine_number": "CNC-001", "department": "Production", "status": "running", "hours_run": 1000},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["machine_number"] == "CNC-001"


def test_get_machines(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/machines", json={"machine_number": "CNC-001", "department": "Production"}, headers=headers)

    response = client.get("/api/machines", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_machine_status(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = client.post("/api/machines", json={"machine_number": "CNC-001", "department": "Production"}, headers=headers)
    machine_id = create_res.json()["id"]

    update_res = client.put(f"/api/machines/{machine_id}", json={"status": "maintenance"}, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "maintenance"


def test_employee_cannot_create_machine(client):
    token = get_token(client, "regularuser", role="employee")
    response = client.post(
        "/api/machines",
        json={"machine_number": "CNC-002", "department": "Production"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403