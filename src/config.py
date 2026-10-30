"""Central configuration for the Data Privacy Pipeline."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SOURCE_DIR = DATA_DIR / "source"
TARGET_DIR = DATA_DIR / "target"
REJECT_DIR = DATA_DIR / "rejects"
AUDIT_DIR = DATA_DIR / "audit"
LOG_DIR = PROJECT_ROOT / "logs"
REPORT_DIR = PROJECT_ROOT / "reports"

CUSTOMER_SOURCE_FILE = SOURCE_DIR / "customer_source.csv"
ORDERS_SOURCE_FILE = SOURCE_DIR / "customer_orders.csv"
CUSTOMER_TARGET_FILE = TARGET_DIR / "analytical_customer.csv"
CUSTOMER_REJECT_FILE = REJECT_DIR / "rejected_records.csv"
ORDER_REJECT_FILE = REJECT_DIR / "invalid_orders.csv"
AUDIT_FILE = AUDIT_DIR / "audit_log.csv"
PIPELINE_LOG_FILE = LOG_DIR / "pipeline.log"
RECONCILIATION_FILE = REPORT_DIR / "reconciliation_report.txt"

MASKING_METHOD = os.getenv("MASKING_METHOD", "mask").strip().lower()
TOKEN_SECRET = os.getenv("TOKEN_SECRET")
RECORD_COUNT = int(os.getenv("RECORD_COUNT", "10000"))
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "123"))

CUSTOMER_COLUMNS = [
    "customer_id", "full_name", "email", "phone",
    "dob", "city", "country", "created_at"
]
ORDER_COLUMNS = ["order_id", "customer_id", "order_amount"]

def ensure_directories():
    """Create all directories required by the pipeline."""
    for directory in (
        SOURCE_DIR, TARGET_DIR, REJECT_DIR, AUDIT_DIR,
        LOG_DIR, REPORT_DIR
    ):
        directory.mkdir(parents=True, exist_ok=True)
