"""Order validation, including primary-key and customer foreign-key checks."""
import pandas as pd
from src.config import ORDER_COLUMNS

class OrderSchemaError(ValueError):
    pass

def validate_orders(orders_df, valid_customer_ids):
    missing = [c for c in ORDER_COLUMNS if c not in orders_df.columns]
    unexpected = [
        c for c in orders_df.columns
        if c not in ORDER_COLUMNS + ["source_file", "source_row_number"]
    ]
    if missing or unexpected:
        raise OrderSchemaError(
            f"Order schema mismatch. Missing={missing}; unexpected={unexpected}"
        )

    work = orders_df.copy()
    reasons = [[] for _ in range(len(work))]

    def add_reason(mask, reason):
        for position, is_bad in enumerate(mask.fillna(False).tolist()):
            if is_bad:
                reasons[position].append(reason)

    order_id = pd.to_numeric(work["order_id"], errors="coerce")
    customer_id = pd.to_numeric(work["customer_id"], errors="coerce")
    amount = pd.to_numeric(work["order_amount"], errors="coerce")

    add_reason(order_id.isna(), "Missing or invalid order_id")
    add_reason(customer_id.isna(), "Missing or invalid customer_id")
    add_reason(amount.isna(), "Missing or invalid order_amount")
    add_reason(amount <= 0, "Order amount must be greater than zero")
    add_reason(work["order_id"].duplicated(keep="first") & work["order_id"].notna(),
               "Duplicate Order ID")
    add_reason(~customer_id.isin(set(valid_customer_ids)), "Invalid Customer Reference")

    work["reject_reason"] = ["; ".join(items) for items in reasons]
    rejected = work[work["reject_reason"] != ""].copy()
    accepted = work[work["reject_reason"] == ""].copy()
    if not accepted.empty:
        accepted["order_id"] = order_id[accepted.index].astype("int64")
        accepted["customer_id"] = customer_id[accepted.index].astype("int64")
        accepted["order_amount"] = amount[accepted.index]
    return accepted.drop(columns=["reject_reason"]), rejected

def validate_referential_integrity():
    """Standalone convenience entry point."""
    from src.config import CUSTOMER_SOURCE_FILE, ORDERS_SOURCE_FILE
    from src.ingest import load_data
    from src.validate import validate_customers
    customers, _ = validate_customers(load_data(CUSTOMER_SOURCE_FILE))
    orders, rejected = validate_orders(
        load_data(ORDERS_SOURCE_FILE), customers["customer_id"].tolist()
    )
    print(f"Valid orders: {len(orders)} | Invalid orders: {len(rejected)}")
    return orders, rejected

if __name__ == "__main__":
    validate_referential_integrity()
