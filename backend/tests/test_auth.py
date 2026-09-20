def test_create_user(client):
    response = client.post("/api/users", json={
        "username": "testadmin",
        "password": "testpass123",
        "role": "admin",
        "employee_id": None
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testadmin"
    assert data["role"] == "admin"
    assert "password" not in data
    assert "password_hash" not in data


def test_create_duplicate_user_fails(client):
    client.post("/api/users", json={
        "username": "testadmin",
        "password": "testpass123",
        "role": "admin"
    })
    response = client.post("/api/users", json={
        "username": "testadmin",
        "password": "differentpass",
        "role": "employee"
    })
    assert response.status_code == 400


def test_login_success(client):
    client.post("/api/users", json={
        "username": "testadmin",
        "password": "testpass123",
        "role": "admin"
    })
    response = client.post("/api/login", data={
        "username": "testadmin",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/api/users", json={
        "username": "testadmin",
        "password": "testpass123",
        "role": "admin"
    })
    response = client.post("/api/login", data={
        "username": "testadmin",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/api/login", data={
        "username": "ghostuser",
        "password": "whatever"
    })
    assert response.status_code == 401