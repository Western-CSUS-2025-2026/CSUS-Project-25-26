import time
from contextlib import contextmanager
from typing import Generator

from prometheus_client import Counter, Histogram


WEBHOOK_FAILURES_TOTAL = Counter(
    'webhook_failures_total',
    'Webhook failures grouped by provider and reason.',
    ['provider', 'reason'],
)

BACKGROUND_TASK_DURATION_SECONDS = Histogram(
    'background_task_duration_seconds',
    'Background task execution duration in seconds.',
    ['task', 'status'],
    buckets=(0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30, 60, 120, 300),
)

BACKGROUND_TASK_FAILURES_TOTAL = Counter(
    'background_task_failures_total',
    'Background task failures grouped by task name.',
    ['task'],
)

EXTERNAL_API_FAILURES_TOTAL = Counter(
    'external_api_failures_total',
    'External API failures grouped by provider, operation and exception type.',
    ['provider', 'operation', 'error_type'],
)


def record_webhook_failure(provider: str, reason: str) -> None:
    WEBHOOK_FAILURES_TOTAL.labels(provider=provider, reason=reason).inc()


def record_external_api_failure(provider: str, operation: str, error: Exception) -> None:
    EXTERNAL_API_FAILURES_TOTAL.labels(
        provider=provider,
        operation=operation,
        error_type=type(error).__name__,
    ).inc()


@contextmanager
def observe_background_task(task_name: str) -> Generator[None, None, None]:
    start = time.perf_counter()
    status = 'success'
    try:
        yield
    except Exception:
        status = 'error'
        BACKGROUND_TASK_FAILURES_TOTAL.labels(task=task_name).inc()
        raise
    finally:
        BACKGROUND_TASK_DURATION_SECONDS.labels(task=task_name, status=status).observe(time.perf_counter() - start)
