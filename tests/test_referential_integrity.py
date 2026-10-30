import pandas as pd
from src.referential_validation import validate_orders

def test_invalid_customer_reference_is_rejected():
    orders = pd.DataFrame([
        {"order_id": 1, "customer_id": 10, "order_amount": 500},
        {"order_id": 2, "customer_id": 99, "order_amount": 300},
    ])
    valid, rejected = validate_orders(orders, [10])
    assert len(valid) == 1
    assert len(rejected) == 1
    assert "Invalid Customer Reference" in rejected.iloc[0]["reject_reason"]

def test_negative_order_amount_is_rejected():
    orders = pd.DataFrame([
        {"order_id": 1, "customer_id": 10, "order_amount": -5}
    ])
    valid, rejected = validate_orders(orders, [10])
    assert valid.empty
    assert "greater than zero" in rejected.iloc[0]["reject_reason"]

def test_duplicate_order_id_is_rejected():
    orders = pd.DataFrame([
        {"order_id": 1, "customer_id": 10, "order_amount": 100},
        {"order_id": 1, "customer_id": 10, "order_amount": 200},
    ])
    valid, rejected = validate_orders(orders, [10])
    assert len(valid) == 1
    assert len(rejected) == 1
