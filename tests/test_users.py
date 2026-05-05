import pytest


def test_create_user(client):
    response = client.post("/users/", json={
        "username": "testuser",
        "age": 25,
        "email": "test@example.com",
        "password": "securepass123",
        "phone": "+1234567890"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["age"] == 25
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_create_user_invalid_age(client):
    response = client.post("/users/", json={
        "username": "younguser",
        "age": 16,
        "email": "young@example.com",
        "password": "password123",
        "phone": "1234567890"
    })
    assert response.status_code == 422  # Validation error


def test_create_user_invalid_email(client):
    response = client.post("/users/", json={
        "username": "invalidemailuser",
        "age": 25,
        "email": "not-an-email",
        "password": "password123",
        "phone": "1234567890"
    })
    assert response.status_code == 422


def test_create_user_duplicate_email(client):
    client.post("/users/", json={
        "username": "user1",
        "age": 30,
        "email": "duplicate@example.com",
        "password": "password123",
        "phone": "1234567890"
    })
    response = client.post("/users/", json={
        "username": "user2",
        "age": 31,
        "email": "duplicate@example.com",
        "password": "password456",
        "phone": "0987654321"
    })
    assert response.status_code == 404  # CustomExceptionB


def test_get_user(client):
    create_response = client.post("/users/", json={
        "username": "getuser",
        "age": 28,
        "email": "get@example.com",
        "password": "password123",
        "phone": "1112223333"
    })
    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "getuser"
    assert data["id"] == user_id


def test_get_nonexistent_user(client):
    response = client.get("/users/99999")
    assert response.status_code == 404


def test_delete_user(client):
    create_response = client.post("/users/", json={
        "username": "deleteuser",
        "age": 35,
        "email": "delete@example.com",
        "password": "password123",
        "phone": "4445556666"
    })
    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_user(client):
    response = client.delete("/users/99999")
    assert response.status_code == 404