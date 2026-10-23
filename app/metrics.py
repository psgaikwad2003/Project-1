"""Prometheus metrics instrumentation for latency, throughput, and system health."""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Standard SRE Golden Signals metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests handled by the service",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency histogram in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)

IN_FLIGHT_REQUESTS = Gauge(
    "http_in_flight_requests",
    "Current number of in-flight HTTP requests",
)

APPLICATION_INFO = Gauge(
    "app_info",
    "Application metadata information",
    ["version", "environment"],
)


def get_latest_metrics() -> tuple[bytes, str]:
    """Generate and return current Prometheus metrics payload."""
    return generate_latest(), CONTENT_TYPE_LATEST
