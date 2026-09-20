def get_token(client, username="testadmin", password="testpass123", role="admin"):
    client.post("/api/users", json={"username": username, "password": password, "role": role})
    response = client.post("/api/login", data={"username": username, "password": password})
    return response.json()["access_token"]


def test_get_employees_requires_auth(client):
    response = client.get("/api/employees")
    assert response.status_code == 401


def test_create_employee(client):
    token = get_token(client)
    response = client.post(
        "/api/employees",
        json={
            "employee_number": "001",
            "name": "Ahmed",
            "email": "ahmed@example.com",
            "position": "Developer",
            "status": "active"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ahmed"
    assert "id" in data


def test_get_employees_after_create(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/api/employees", json={
        "employee_number": "001", "name": "Ahmed", "email": "ahmed@example.com"
    }, headers=headers)

    response = client.get("/api/employees", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_employee(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = client.post("/api/employees", json={
        "employee_number": "001", "name": "Ahmed", "email": "ahmed@example.com"
    }, headers=headers)
    employee_id = create_res.json()["id"]

    update_res = client.put(f"/api/employees/{employee_id}", json={
        "employee_number": "001", "name": "Ahmed Updated", "email": "ahmed@example.com"
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Ahmed Updated"


def test_delete_employee(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    create_res = client.post("/api/employees", json={
        "employee_number": "001", "name": "Ahmed", "email": "ahmed@example.com"
    }, headers=headers)
    employee_id = create_res.json()["id"]

    delete_res = client.delete(f"/api/employees/{employee_id}", headers=headers)
    assert delete_res.status_code == 200

    get_res = client.get(f"/api/employees/{employee_id}", headers=headers)
    assert get_res.status_code == 404


def test_get_nonexistent_employee(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/employees/999", headers=headers)
    assert response.status_code == 404