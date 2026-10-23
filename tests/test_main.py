"""Unit and integration test suite for CloudOps Nexus API."""

import pytest
from fastapi.testclient import TestClient
from app.main import app, TASKS_DB


@pytest.fixture
def client():
    """Test client fixture with clean test database state."""
    TASKS_DB.clear()
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint(client):
    """Test root endpoint returns service metadata and status 200."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert data["health_check"] == "/healthz"


def test_liveness_probe(client):
    """Test liveness probe returns healthy status and 200."""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_readiness_probe(client):
    """Test readiness probe verifies dependencies."""
    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["dependencies"]["database"] == "connected"


def test_prometheus_metrics(client):
    """Test metrics endpoint outputs valid Prometheus text format."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text


def test_task_lifecycle(client):
    """Test full CRUD lifecycle for task management."""
    # 1. Initially empty
    res_list = client.get("/api/v1/tasks")
    assert res_list.status_code == 200
    assert res_list.json() == []

    # 2. Create task
    task_payload = {
        "title": "Configure EKS Ingress",
        "description": "Deploy AWS Load Balancer Controller with cert-manager",
        "completed": False,
    }
    res_create = client.post("/api/v1/tasks", json=task_payload)
    assert res_create.status_code == 201
    created_task = res_create.json()
    task_id = created_task["id"]
    assert created_task["title"] == task_payload["title"]

    # 3. Retrieve task
    res_get = client.get(f"/api/v1/tasks/{task_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == task_id

    # 4. Get non-existent task
    res_not_found = client.get("/api/v1/tasks/non-existent-id")
    assert res_not_found.status_code == 404
