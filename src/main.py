"""Orchestrate the customer privacy pipeline."""
import logging
import time
from datetime import datetime, timezone
import pandas as pd

from src.config import (
    CUSTOMER_SOURCE_FILE, ORDERS_SOURCE_FILE, CUSTOMER_TARGET_FILE,
    CUSTOMER_REJECT_FILE, ORDER_REJECT_FILE, PIPELINE_LOG_FILE,
    RECONCILIATION_FILE, ensure_directories
)
from src.ingest import load_data
from src.validate import validate_customers
from src.referential_validation import validate_orders
from src.transform import transform_email
from src.publish import save_output
from src.audit import write_audit_log

def configure_logging():
    ensure_directories()
    logging.basicConfig(
        filename=PIPELINE_LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        force=True,
    )

def run_pipeline():
    ensure_directories()
    configure_logging()
    start_time = datetime.now(timezone.utc)
    timer = time.perf_counter()
    customer_input_count = 0
    customer_output_count = 0
    customer_rejected_count = 0
    status = "FAILED"
    failure_reason = ""

    try:
        logging.info("Pipeline started")
        customers_raw = load_data(CUSTOMER_SOURCE_FILE)
        customer_input_count = len(customers_raw)
        customers_valid, customers_rejected = validate_customers(customers_raw)

        orders_raw = load_data(ORDERS_SOURCE_FILE)
        orders_valid, orders_rejected = validate_orders(
            orders_raw, customers_valid["customer_id"].tolist()
        )

        # Keep only fields needed by the analytical consumer.
        target = customers_valid[
            ["customer_id", "email", "city", "country", "created_at"]
        ].copy()
        target["email"] = target["email"].apply(transform_email)

        # Publish the target only after validation and transformation succeed.
        save_output(target, CUSTOMER_TARGET_FILE)
        save_output(customers_rejected, CUSTOMER_REJECT_FILE)
        save_output(orders_rejected, ORDER_REJECT_FILE)

        customer_output_count = len(target)
        customer_rejected_count = len(customers_rejected)
        status = "SUCCESS"

        elapsed = time.perf_counter() - timer
        report = [
            "DATA PRIVACY PIPELINE RECONCILIATION",
            f"run_started_utc: {start_time.isoformat()}",
            f"customer_input_count: {customer_input_count}",
            f"customer_output_count: {customer_output_count}",
            f"customer_rejected_count: {customer_rejected_count}",
            f"customer_reconciliation_passed: "
            f"{customer_input_count == customer_output_count + customer_rejected_count}",
            f"orders_input_count: {len(orders_raw)}",
            f"orders_valid_count: {len(orders_valid)}",
            f"orders_rejected_count: {len(orders_rejected)}",
            f"orders_reconciliation_passed: "
            f"{len(orders_raw) == len(orders_valid) + len(orders_rejected)}",
            f"execution_seconds: {elapsed:.6f}",
        ]
        RECONCILIATION_FILE.parent.mkdir(parents=True, exist_ok=True)
        RECONCILIATION_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")
        logging.info("Pipeline completed successfully in %.6f seconds", elapsed)
        print("\n".join(report))
        return target

    except Exception as exc:
        failure_reason = f"{type(exc).__name__}: {exc}"
        logging.exception("Pipeline failed: %s", failure_reason)
        raise
    finally:
        end_time = datetime.now(timezone.utc)
        try:
            write_audit_log(
                input_count=customer_input_count,
                output_count=customer_output_count,
                rejected_count=customer_rejected_count,
                status=status,
                start_time=start_time,
                end_time=end_time,
                failure_reason=failure_reason,
                source_file=CUSTOMER_SOURCE_FILE,
            )
        except Exception:
            logging.exception("Could not write audit log")

if __name__ == "__main__":
    run_pipeline()
