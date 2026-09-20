def get_token(client, username, password="testpass123", role="employee"):
    client.post("/api/users", json={"username": username, "password": password, "role": role})
    response = client.post("/api/login", data={"username": username, "password": password})
    return response.json()["access_token"]


def create_employee(client, token, employee_number="001"):
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post("/api/employees", json={
        "employee_number": employee_number,
        "name": "Test Employee",
        "email": f"{employee_number}@example.com"
    }, headers=headers)
    return res.json()["id"]


def test_create_ticket(client):
    admin_token = get_token(client, "adminuser", role="admin")
    emp_id = create_employee(client, admin_token)

    token = get_token(client, "employee1", role="employee")
    response = client.post(
        "/api/tickets",
        json={"employee_id": emp_id, "title": "Laptop won't turn on", "priority": "high"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Laptop won't turn on"
    assert data["status"] == "open"


def test_admin_sees_all_tickets(client):
    admin_token = get_token(client, "adminuser", role="admin")
    emp_id = create_employee(client, admin_token)
    emp_token = get_token(client, "employee1", role="employee")

    client.post("/api/tickets", json={"employee_id": emp_id, "title": "Issue A"},
                headers={"Authorization": f"Bearer {emp_token}"})
    client.post("/api/tickets", json={"employee_id": emp_id, "title": "Issue B"},
                headers={"Authorization": f"Bearer {admin_token}"})

    response = client.get("/api/tickets", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_it_staff_can_update_ticket_status(client):
    admin_token = get_token(client, "adminuser", role="admin")
    emp_id = create_employee(client, admin_token)
    it_token = get_token(client, "itstaffuser", role="it_staff")

    create_res = client.post("/api/tickets", json={"employee_id": emp_id, "title": "Network down"},
                              headers={"Authorization": f"Bearer {admin_token}"})
    ticket_id = create_res.json()["id"]

    update_res = client.put(f"/api/tickets/{ticket_id}", json={"status": "in_progress"},
                             headers={"Authorization": f"Bearer {it_token}"})
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "in_progress"


def test_update_nonexistent_ticket(client):
    token = get_token(client, "adminuser", role="admin")
    response = client.put("/api/tickets/999", json={"status": "resolved"},
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404