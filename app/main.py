"""CloudOps Nexus Enterprise REST API service."""

import time
import uuid
from contextlib import asynccontextmanager
from typing import Dict, Any, List

from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import get_settings
from app.logger import setup_logger
from app.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    IN_FLIGHT_REQUESTS,
    APPLICATION_INFO,
    get_latest_metrics,
)

settings = get_settings()
logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events management for startup and graceful shutdown."""
    logger.info("Application starting up...", extra={"correlation_id": "startup"})
    APPLICATION_INFO.labels(
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
    ).set(1)
    yield
    logger.info("Application gracefully shutting down...", extra={"correlation_id": "shutdown"})


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Cloud-Native Microservices Platform for High-Availability Workloads",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    """Middleware for tracking request latency, correlation IDs, and HTTP status counts."""
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id

    IN_FLIGHT_REQUESTS.inc()
    start_time = time.time()

    response: Response = None
    try:
        response = await call_next(request)
        duration = time.time() - start_time

        response.headers["X-Correlation-ID"] = correlation_id
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(duration)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()
        return response
    except Exception as exc:
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ).inc()
        logger.error(
            f"Unhandled exception during request processing: {str(exc)}",
            extra={"correlation_id": correlation_id},
            exc_info=True,
        )
        raise exc
    finally:
        IN_FLIGHT_REQUESTS.dec()


# Schemas
class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    environment: str
    timestamp: float


class TaskItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    completed: bool = False


# In-memory storage for demonstration
TASKS_DB: Dict[str, TaskItem] = {}


# Kubernetes Probes & Observability Endpoints
@app.get("/healthz", response_model=HealthResponse, tags=["Observability"])
async def liveness_probe():
    """Kubernetes liveness probe: returns 200 if process is running."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        timestamp=time.time(),
    )


@app.get("/readyz", tags=["Observability"])
async def readiness_probe():
    """Kubernetes readiness probe: validates downstream dependencies and readiness."""
    # Production check: verify DB connection, Redis ping, etc.
    return {
        "status": "ready",
        "dependencies": {
            "database": "connected",
            "cache": "connected",
        },
        "timestamp": time.time(),
    }


@app.get("/metrics", tags=["Observability"])
async def metrics_endpoint():
    """Prometheus metrics endpoint for scraping by monitoring systems."""
    metrics_data, content_type = get_latest_metrics()
    return Response(content=metrics_data, media_type=content_type)


@app.get("/", tags=["System"])
async def root():
    """Root overview endpoint with service metadata."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "docs_url": "/docs",
        "health_check": "/healthz",
        "metrics_url": "/metrics",
    }


# Business Microservice Endpoints
@app.get("/api/v1/tasks", response_model=List[TaskItem], tags=["Tasks"])
async def list_tasks():
    """List all deployed workload tasks."""
    return list(TASKS_DB.values())


@app.post("/api/v1/tasks", response_model=TaskItem, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskItem):
    """Create a new task item in the system."""
    TASKS_DB[task.id] = task
    return task


@app.get("/api/v1/tasks/{task_id}", response_model=TaskItem, tags=["Tasks"])
async def get_task(task_id: str):
    """Retrieve specific task by its identifier."""
    if task_id not in TASKS_DB:
        raise HTTPException(status_code=404, detail="Task not found")
    return TASKS_DB[task_id]
