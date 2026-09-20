def get_token(client, username, password="testpass123", role="employee"):
    client.post("/api/users", json={"username": username, "password": password, "role": role})
    response = client.post("/api/login", data={"username": username, "password": password})
    return response.json()["access_token"]


def test_employee_cannot_create_department(client):
    token = get_token(client, "regularuser", role="employee")
    response = client.post(
        "/api/departments",
        json={"name": "IT", "manager": "Someone"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_admin_can_create_department(client):
    token = get_token(client, "adminuser", role="admin")
    response = client.post(
        "/api/departments",
        json={"name": "IT", "manager": "Someone"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_employee_cannot_create_asset(client):
    token = get_token(client, "regularuser", role="employee")
    response = client.post(
        "/api/assets",
        json={"asset_number": "AST-001", "asset_type": "Laptop", "name": "Dell"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_it_staff_can_create_asset(client):
    token = get_token(client, "itstaffuser", role="it_staff")
    response = client.post(
        "/api/assets",
        json={"asset_number": "AST-001", "asset_type": "Laptop", "name": "Dell"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_employee_can_view_departments(client):
    token = get_token(client, "regularuser", role="employee")
    response = client.get(
        "/api/departments",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_employee_cannot_update_ticket_status(client):
    admin_token = get_token(client, "adminuser", role="admin")
    emp_token = get_token(client, "regularuser", role="employee")

    emp_res = client.post("/api/employees", json={
        "employee_number": "001", "name": "Test", "email": "test@example.com"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    emp_id = emp_res.json()["id"]

    ticket_res = client.post(
        "/api/tickets",
        json={"employee_id": emp_id, "title": "Laptop broken", "priority": "high"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    ticket_id = ticket_res.json()["id"]

    response = client.put(
        f"/api/tickets/{ticket_id}",
        json={"status": "resolved"},
        headers={"Authorization": f"Bearer {emp_token}"}
    )
    assert response.status_code == 403