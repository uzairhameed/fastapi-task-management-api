
# ============================================================
# STAGE 1: BUILDER
# Purpose: Create a virtual environment and install dependencies.
# ============================================================

# Start with a lightweight Python 3.11 image.
# "builder" is the name of this stage.
FROM python:3.11-slim AS builder

# Set the working directory inside this stage.
# Subsequent relative paths will use /build.
WORKDIR /build

# Create an isolated Python virtual environment.
# This keeps our application's dependencies separate from system Python.
RUN python -m venv /opt/venv

# Put the virtual environment's executables first in PATH.
# This lets "pip" and Python packages use /opt/venv by default.
ENV PATH="/opt/venv/bin:$PATH"

# Copy only requirements.txt first.
# Docker can reuse the dependency-installation layer when application
# source code changes but requirements.txt stays the same.
COPY requirements.txt .

# Install all Python dependencies into the virtual environment.
# --no-cache-dir prevents pip from retaining its download cache in the image.
RUN pip install --no-cache-dir -r requirements.txt


# ============================================================
# STAGE 2: RUNTIME
# Purpose: Run the application without carrying the builder stage along.
# ============================================================

# Start a fresh, lightweight image for running the API.
FROM python:3.11-slim AS runtime

# Set the application's working directory inside the container.
WORKDIR /app

# Configure Python and package execution.
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy the installed virtual environment from the builder stage.
# We copy the dependencies, not the builder's entire filesystem.
COPY --from=builder /opt/venv /opt/venv

# Copy the FastAPI application source code.
COPY app/ ./app/

# Copy Alembic migration scripts and configuration.
# These will be needed when we run database migrations.
COPY alembic/ ./alembic/
COPY alembic.ini .

# Create a non-root user and give it ownership of the application directory.
# Running as a regular user reduces the damage possible if the application
# is compromised.
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app

# Switch from root to the unprivileged application user.
# The application process will run as appuser.
USER appuser

# Document that the application listens on port 8000.
# This does not itself publish the port to the host.
EXPOSE 8000

# Start the FastAPI application using Uvicorn.
# 0.0.0.0 allows connections to the application through the container's
# network interface, rather than only from inside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

