
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import ALLOWED_ORIGINS
from app.core.middleware import request_logging_middleware
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.core.exceptions import register_exception_handlers
from app.modules.tasks.router import router as tasks_router


app = FastAPI(
    title="Task Management API",
    description="A REST API for managing personal tasks",
    version="1.0.0",
)

register_exception_handlers(app)

# Configure Cross-Origin Resource Sharing (CORS).
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log HTTP method, path, response status, and request duration.
# Avoid logging request bodies or credentials.
app.middleware("http")(request_logging_middleware)

# Register feature routers.
app.include_router(users_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Task Management Api is running"}
