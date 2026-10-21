
from uuid import uuid4


def test_create_task(client):
    unique_id = uuid4().hex[:8]
    username = f"taskuser_{unique_id}"
    email = f"taskuser_{unique_id}@example.com"
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

    # Log in to obtain a JWT.
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task.
    response = client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={
            "title": "Write automated tests",
            "description": "Test task creation with pytest",
            "status": "pending",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Write automated tests"
    assert data["description"] == "Test task creation with pytest"
    assert data["status"] == "pending"
    assert data["owner_id"] == register_response.json()["id"]
    assert "id" in data


def test_get_tasks(client):
    unique_id = uuid4().hex[:8]
    username = f"listuser_{unique_id}"
    email = f"listuser_{unique_id}@example.com"
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

    # Log in.
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task for this user.
    create_response = client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={
            "title": "Test task listing",
            "description": "Verify that the task appears in the list",
            "status": "pending",
        },
    )
    assert create_response.status_code == 201

    # Fetch the user's tasks.
    response = client.get("/api/v1/tasks/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(
        task["id"] == create_response.json()["id"]
        for task in response.json()
    )


def test_user_cannot_access_another_users_task(client):
    password = "SecurePass123!"

    # Register two different users.
    user_a_id = uuid4().hex[:8]
    user_b_id = uuid4().hex[:8]

    user_a = {
        "username": f"owner_{user_a_id}",
        "email": f"owner_{user_a_id}@example.com",
        "password": password,
    }
    user_b = {
        "username": f"other_{user_b_id}",
        "email": f"other_{user_b_id}@example.com",
        "password": password,
    }

    response_a = client.post("/api/v1/users/", json=user_a)
    response_b = client.post("/api/v1/users/", json=user_b)

    assert response_a.status_code == 201
    assert response_b.status_code == 201

    # Log in as User A.
    login_a = client.post(
        "/api/v1/auth/login",
        data={"username": user_a["username"], "password": password},
    )
    assert login_a.status_code == 200
    headers_a = {
        "Authorization": f"Bearer {login_a.json()['access_token']}"
    }

    # Log in as User B.
    login_b = client.post(
        "/api/v1/auth/login",
        data={"username": user_b["username"], "password": password},
    )
    assert login_b.status_code == 200
    headers_b = {
        "Authorization": f"Bearer {login_b.json()['access_token']}"
    }

    # User A creates a task.
    task_response = client.post(
        "/api/v1/tasks/",
        headers=headers_a,
        json={"title": "Private task", "status": "pending"},
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    # User B must not be able to retrieve User A's task.
    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers_b,
    )

    assert response.status_code == 404


def test_get_tasks_filtered_by_status(client):
    unique_id = uuid4().hex[:8]
    username = f"filter_{unique_id}"
    email = f"filter_{unique_id}@example.com"
    password = "SecurePass123!"

    # Register and log in.
    register_response = client.post(
        "/api/v1/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Create one pending task and one completed task.
    for title, task_status in [
        ("Pending task", "pending"),
        ("Completed task", "done"),
    ]:
        response = client.post(
            "/api/v1/tasks/",
            headers=headers,
            json={"title": title, "status": task_status},
        )
        assert response.status_code == 201

    # Request only pending tasks.
    response = client.get(
        "/api/v1/tasks/",
        headers=headers,
        params={"status": "pending"},
    )

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Pending task"
    assert tasks[0]["status"] == "pending"


def test_update_task(client):
    unique_id = uuid4().hex[:8]
    username = f"update_{unique_id}"
    email = f"update_{unique_id}@example.com"
    password = "SecurePass123!"

    # Register and log in.
    register_response = client.post(
        "/api/v1/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Create a task.
    create_response = client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={"title": "Original title", "status": "pending"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Update the task's title and status.
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
        json={
            "title": "Updated title",
            "status": "in_progress",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["status"] == "in_progress"
    assert data["id"] == task_id


def test_delete_task(client):
    unique_id = uuid4().hex[:8]
    username = f"delete_{unique_id}"
    email = f"delete_{unique_id}@example.com"
    password = "SecurePass123!"

    # Register and log in.
    register_response = client.post(
        "/api/v1/users/",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    # Create a task.
    create_response = client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={"title": "Task to delete", "status": "pending"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Delete the task.
    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    # Confirm the task can no longer be retrieved.
    get_response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=headers,
    )
    assert get_response.status_code == 404
