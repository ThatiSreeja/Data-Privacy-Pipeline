import pandas as pd
import pytest
from src.validate import validate_email, validate_customers, SchemaValidationError

def sample_customer(**changes):
    row = {
        "customer_id": 1, "full_name": "A Person",
        "email": "a@gmail.com", "phone": "9876543210",
        "dob": "1995-01-01", "city": "Hyderabad",
        "country": "India", "created_at": "2026-01-01",
    }
    row.update(changes)
    return row

def test_valid_email():
    assert validate_email("abc@gmail.com") is True

def test_invalid_email():
    assert validate_email("abcgmail.com") is False

def test_missing_email_is_rejected():
    valid, rejected = validate_customers(pd.DataFrame([sample_customer(email=None)]))
    assert len(valid) == 0
    assert "Missing Email" in rejected.iloc[0]["reject_reason"]

def test_duplicate_customer_id_is_rejected():
    valid, rejected = validate_customers(pd.DataFrame([
        sample_customer(), sample_customer(email="second@gmail.com")
    ]))
    assert len(valid) == 1
    assert len(rejected) == 1
    assert "Duplicate Customer ID" in rejected.iloc[0]["reject_reason"]

def test_empty_input_is_supported():
    columns = [
        "customer_id", "full_name", "email", "phone",
        "dob", "city", "country", "created_at"
    ]
    valid, rejected = validate_customers(pd.DataFrame(columns=columns))
    assert valid.empty and rejected.empty

def test_unexpected_schema_column_fails():
    row = sample_customer()
    row["unexpected"] = "value"
    with pytest.raises(SchemaValidationError):
        validate_customers(pd.DataFrame([row]))

def test_invalid_date_is_rejected():
    valid, rejected = validate_customers(
        pd.DataFrame([sample_customer(created_at="not-a-date")])
    )
    assert valid.empty
    assert "Invalid created_at" in rejected.iloc[0]["reject_reason"]
