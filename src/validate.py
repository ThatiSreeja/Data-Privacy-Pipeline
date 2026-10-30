"""Customer schema and business-rule validation."""
import re
import pandas as pd
from src.config import CUSTOMER_COLUMNS

class SchemaValidationError(ValueError):
    pass

_EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")

def validate_email(email):
    if pd.isna(email):
        return False
    return bool(_EMAIL_PATTERN.match(str(email).strip()))

def validate_customer_schema(df):
    missing = [column for column in CUSTOMER_COLUMNS if column not in df.columns]
    unexpected = [
        column for column in df.columns
        if column not in CUSTOMER_COLUMNS + ["source_file", "source_row_number"]
    ]
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing columns: {missing}")
        if unexpected:
            details.append(f"unexpected columns: {unexpected}")
        raise SchemaValidationError("; ".join(details))

def validate_customers(df):
    """Return (accepted_customers, rejected_customers). First duplicate key wins."""
    validate_customer_schema(df)
    work = df.copy()
    reasons = [[] for _ in range(len(work))]

    def add_reason(mask, reason):
        for position, is_bad in enumerate(mask.fillna(False).tolist()):
            if is_bad:
                reasons[position].append(reason)

    numeric_id = pd.to_numeric(work["customer_id"], errors="coerce")
    add_reason(numeric_id.isna(), "Missing or non-numeric customer_id")
    add_reason(work["email"].isna(), "Missing Email")
    add_reason(~work["email"].apply(validate_email), "Invalid Email")
    for field in ("full_name", "phone", "city", "country", "created_at"):
        add_reason(work[field].isna(), f"Missing {field}")

    # Detect duplicate non-null IDs; preserve the first occurrence.
    duplicate_mask = work["customer_id"].duplicated(keep="first") & work["customer_id"].notna()
    add_reason(duplicate_mask, "Duplicate Customer ID")

    # Validate date fields without silently accepting malformed dates.
    for field in ("dob", "created_at"):
        parsed = pd.to_datetime(work[field], errors="coerce")
        add_reason(parsed.isna(), f"Invalid {field}")

    work["reject_reason"] = ["; ".join(items) for items in reasons]
    rejected = work[work["reject_reason"] != ""].copy()
    accepted = work[work["reject_reason"] == ""].copy()
    accepted["customer_id"] = pd.to_numeric(accepted["customer_id"]).astype("int64")
    return accepted.drop(columns=["reject_reason"]), rejected

def validate_data(df):
    """Backward-compatible wrapper returning rejected rows as dictionaries."""
    _, rejected = validate_customers(df)
    return rejected.to_dict(orient="records")

if __name__ == "__main__":
    from src.config import CUSTOMER_SOURCE_FILE
    from src.ingest import load_data
    accepted, rejected = validate_customers(load_data(CUSTOMER_SOURCE_FILE))
    print(f"Accepted: {len(accepted)} | Rejected: {len(rejected)}")
