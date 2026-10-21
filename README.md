# FastAPI Task Management API

A Task Management REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. It provides JWT-based authentication, user-specific task management, status filtering, database migrations, and automated tests.

## Features

- User registration with securely hashed passwords
- Login with JWT access tokens
- Protected endpoints for authenticated users
- Create, read, update, and delete tasks
- Filter tasks by status: `pending`, `in_progress`, and `done`
- Server-side task ownership and access control
- PostgreSQL integration with SQLAlchemy
- Database schema migrations with Alembic
- CORS configuration for local frontend development
- Global exception handling and request logging
- Automated API tests with pytest

## Tech Stack

- **Backend:** FastAPI, Python
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT, pwdlib/Argon2
- **Migrations:** Alembic
- **Testing:** pytest, FastAPI TestClient

## Project Structure

```text
app/
├── main.py
├── database.py
├── core/
│   ├── config.py
│   ├── security.py
│   ├── dependencies.py
│   ├── middleware.py
│   └── exceptions.py
└── modules/
    ├── auth/
    ├── users/
    └── tasks/

alembic/
tests/
├── conftest.py
├── test_main.py
├── test_users.py
├── test_auth.py
└── test_tasks.py

alembic.ini
requirements.txt
```

## Prerequisites

- Python 3.11+
- PostgreSQL
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-task-management-api.git
cd fastapi-task-management-api
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/task_management_db
JWT_SECRET_KEY=replace_with_a_secure_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Update the database credentials to match your PostgreSQL configuration. Use a strong, randomly generated JWT secret. Never commit your `.env` file or real secrets to GitHub.

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

The API will run at:

- API base URL: `http://127.0.0.1:8000`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/v1/users/` | Register a user | No |
| POST | `/api/v1/auth/login` | Log in and receive a JWT | No |
| GET | `/api/v1/auth/me` | Get current user details | Yes |
| POST | `/api/v1/tasks/` | Create a task | Yes |
| GET | `/api/v1/tasks/` | List the current user's tasks | Yes |
| GET | `/api/v1/tasks/{task_id}` | Retrieve a task | Yes |
| PATCH | `/api/v1/tasks/{task_id}` | Update a task | Yes |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task | Yes |

To filter tasks by status, use a query parameter such as:

```text
GET /api/v1/tasks/?status=pending
```

For protected endpoints, send the JWT in the request header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

The login endpoint accepts form data with `username` and `password`.

## Running Tests

Run the automated test suite from the project root:

```bash
python -m pytest -v
```

The current suite covers registration, authentication, task CRUD operations, status filtering, and task ownership.

**Note:** Tests currently use the configured database. Test records may remain in that database after execution.

## Security Notes

- Passwords are stored as hashes rather than plaintext.
- Protected endpoints require valid JWT authentication.
- Users can access and modify only their own tasks.
- Keep `.env`, database credentials, and JWT secrets out of version control.

## License

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
