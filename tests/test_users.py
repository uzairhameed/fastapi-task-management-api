from uuid import uuid4


def test_register_user(client):
    unique_id = uuid4().hex[:8]
    username = f"pytest_{unique_id}"
    email = f"pytest_{unique_id}@example.com"

    response = client.post(
        "/api/v1/users/",
        json={
            "username": username,
            "email": email,
            "password": "SecurePass123!",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["username"] == username
    assert data["email"] == email
    assert data["is_active"] is True
    assert "password" not in data
    assert "hashed_password" not in data
