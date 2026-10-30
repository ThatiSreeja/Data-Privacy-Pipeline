"""Generate deterministic synthetic customer and order CSV files."""
import random
import pandas as pd
from faker import Faker

from src.config import (
    CUSTOMER_SOURCE_FILE, ORDERS_SOURCE_FILE,
    RECORD_COUNT, RANDOM_SEED, ensure_directories
)

def generate_data(record_count=RECORD_COUNT, seed=RANDOM_SEED):
    if record_count < 0:
        raise ValueError("record_count cannot be negative")

    ensure_directories()
    rng = random.Random(seed)
    fake = Faker("en_IN")
    Faker.seed(seed)

    customers = []
    for customer_id in range(1, record_count + 1):
        row = {
            "customer_id": customer_id,
            "full_name": fake.name(),
            "email": fake.email(),
            "phone": fake.msisdn()[-10:],
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=85).isoformat(),
            "city": fake.city(),
            "country": "India",
            "created_at": fake.date_this_year().isoformat(),
        }
        # Deliberately labelled invalid scenarios, kept reproducible.
        scenario = rng.random()
        if scenario < 0.005:
            row["email"] = None                 # missing email
        elif scenario < 0.010:
            row["email"] = "invalidemail.com"  # malformed email
        elif scenario < 0.015 and customers:
            row["customer_id"] = customers[-1]["customer_id"]  # duplicate key
        customers.append(row)

    orders = []
    for order_id in range(1, max(1, record_count // 20) + 1):
        customer_id = rng.randint(1, max(1, record_count))
        amount = rng.randint(100, 5000)
        if order_id <= min(10, max(1, record_count // 20)):
            customer_id = record_count + 100  # deliberately invalid reference
        if order_id == 11:
            amount = -50                       # domain-specific invalid amount
        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_amount": amount,
        })

    pd.DataFrame(customers).to_csv(CUSTOMER_SOURCE_FILE, index=False)
    pd.DataFrame(orders, columns=["order_id", "customer_id", "order_amount"]).to_csv(
        ORDERS_SOURCE_FILE, index=False
    )
    print(f"Generated {len(customers)} customers and {len(orders)} orders.")
    print(f"Customer file: {CUSTOMER_SOURCE_FILE}")
    print(f"Orders file: {ORDERS_SOURCE_FILE}")

if __name__ == "__main__":
    generate_data()
