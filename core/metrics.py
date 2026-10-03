METRICS = {
    "run_count": 0,
    "agents_selected": 0,
    "agent_calls": 0,
    "mcp_calls": 0,
    "replanning_events": 0,
    "approval_required": 0,
    "approvals": 0,
    "rejections": 0,
    "total_runtime_seconds": 0.0
}


def increment(metric, amount=1):
    METRICS[metric] += amount


def add_runtime(seconds):
    METRICS["total_runtime_seconds"] += seconds


def get_metrics():
    return METRICS.copy()


def reset_metrics():
    for key in METRICS:
        METRICS[key] = 0