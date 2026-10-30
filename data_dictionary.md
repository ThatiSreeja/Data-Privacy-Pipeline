# Data Dictionary

## Customer source (`data/source/customer_source.csv`)
Grain: one row per customer. Primary key: `customer_id`.

| Column | Type | Nullable | Description |
|---|---|---:|---|
| customer_id | integer | No | Stable customer identifier |
| full_name | string | No | Synthetic customer name; sensitive |
| email | string | No | Customer email; sensitive |
| phone | string | No | Customer phone; sensitive |
| dob | date | No | Date of birth; sensitive |
| city | string | No | City |
| country | string | No | Country |
| created_at | date | No | Customer creation date |

## Orders source (`data/source/customer_orders.csv`)
Grain: one row per order. Primary key: `order_id`. Foreign key: `customer_id` references accepted customer IDs.

| Column | Type | Nullable | Description |
|---|---|---:|---|
| order_id | integer | No | Order identifier |
| customer_id | integer | No | Customer foreign key |
| order_amount | decimal/integer | No | Must be greater than zero |

## Analytical target
Columns: `customer_id`, transformed `email`, `city`, `country`, `created_at`.
Full name, phone and date of birth are excluded by data minimization.

## Reject records
Rejected rows retain original source columns plus `source_file`, `source_row_number`, and `reject_reason`.
