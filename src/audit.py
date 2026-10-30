"""Append-only pipeline audit logging."""
import uuid
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

AUDIT_COLUMNS = [
    "run_id", "start_time", "end_time", "duration_seconds",
    "input_count", "output_count", "rejected_count", "status",
    "failure_reason", "source_file"
]

def write_audit_log(
    input_count, output_count, rejected_count, status,
    start_time, end_time=None, failure_reason="", source_file=""
):
    end_time = end_time or datetime.now(timezone.utc)
    duration = max(0.0, (end_time - start_time).total_seconds())
    row = {
        "run_id": str(uuid.uuid4()),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": round(duration, 6),
        "input_count": int(input_count),
        "output_count": int(output_count),
        "rejected_count": int(rejected_count),
        "status": status,
        "failure_reason": str(failure_reason),
        "source_file": str(source_file),
    }
    path = Path(__file__).resolve().parent.parent / "data" / "audit" / "audit_log.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row], columns=AUDIT_COLUMNS).to_csv(
        path, mode="a", header=not path.exists(), index=False
    )
    return row["run_id"]
