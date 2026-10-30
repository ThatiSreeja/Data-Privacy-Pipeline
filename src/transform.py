"""Privacy transformations. HMAC tokenization is deterministic and keyed."""
import hashlib
import hmac
import pandas as pd
from src.config import MASKING_METHOD, TOKEN_SECRET

def mask_email(email):
    if pd.isna(email) or "@" not in str(email):
        return "INVALID_EMAIL"
    username, domain = str(email).strip().split("@", 1)
    if not username:
        return "***@" + domain
    return username[0] + "***@" + domain

def mask_phone(phone):
    if pd.isna(phone):
        return "INVALID_PHONE"
    digits = "".join(ch for ch in str(phone) if ch.isdigit())
    return "******" + digits[-4:] if digits else "INVALID_PHONE"

def tokenize(value, secret=None):
    key = secret or TOKEN_SECRET
    if not key:
        raise ValueError(
            "TOKEN_SECRET must be set in the environment when MASKING_METHOD=tokenize"
        )
    return hmac.new(
        key.encode("utf-8"), str(value).encode("utf-8"), hashlib.sha256
    ).hexdigest()

def transform_email(email, method=None):
    selected = (method or MASKING_METHOD).lower()
    if selected == "mask":
        return mask_email(email)
    if selected == "tokenize":
        if pd.isna(email):
            return "INVALID_EMAIL"
        return tokenize(email)
    raise ValueError("MASKING_METHOD must be either 'mask' or 'tokenize'")
