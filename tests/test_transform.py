import pytest
from src.transform import mask_email, mask_phone, tokenize, transform_email

def test_mask_email():
    assert mask_email("john@gmail.com") == "j***@gmail.com"

def test_mask_phone():
    assert mask_phone("9876543210") == "******3210"

def test_tokenize_is_deterministic():
    assert tokenize("customer-1", "test-secret") == tokenize("customer-1", "test-secret")

def test_tokenize_changes_with_secret():
    assert tokenize("customer-1", "secret-a") != tokenize("customer-1", "secret-b")

def test_transform_rejects_unknown_method():
    with pytest.raises(ValueError):
        transform_email("a@gmail.com", "unknown")
