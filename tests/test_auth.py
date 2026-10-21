
from uuid import uuid4


def test_login_user(client):
    unique_id = uuid4().hex[:8]
    username = f"login_{unique_id}"
    email = f"login_{unique_id}@example.com"
    password = "SecurePass123!"

    # Register a unique user for this test.
    register_response = client.post(
        "/api/v1/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    # Login using form data, as required by OAuth2PasswordRequestForm.
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["token_type"].lower() == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_login_wrong_password(client):
    unique_id = uuid4().hex[:8]
    username = f"wrongpass_{unique_id}"
    email = f"wrongpass_{unique_id}@example.com"
    password = "SecurePass123!"

    # Register a user first.
    register_response = client.post(
        "/api/v1/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    # Attempt login with an incorrect password.
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": username,
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
    assert response.headers["www-authenticate"] == "Bearer"


def test_get_current_user(client):
    unique_id = uuid4().hex[:8]
    username = f"current_{unique_id}"
    email = f"current_{unique_id}@example.com"
    password = "SecurePass123!"

    # Register a user.
    register_response = client.post(
        "/api/v1/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    # Log in to obtain an access token.
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Access the protected endpoint using the token.
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == username
    assert response.json()["email"] == email
    assert "id" in response.json()


def test_get_current_user_without_token(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
