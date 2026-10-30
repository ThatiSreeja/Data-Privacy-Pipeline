Data Privacy Pipeline

Project Overview

This project is developed using Python to process customer and order data while protecting sensitive information.

It checks data quality, identifies invalid records, masks customer email addresses, and stores valid and rejected records separately.

Technologies Used

Python
Pandas
Faker
Pytest



Project Structure

Data_Privacy_Pipeline/
│
├── src/
│   ├── config.py
│   ├── generate_data.py
│   ├── ingest.py
│   ├── validate.py
│   ├── referential_validation.py
│   ├── transform.py
│   ├── publish.py
│   ├── audit.py
│   └── main.py
│
├── tests/
├── data/
│   ├── source/
│   ├── target/
│   ├── rejects/
│   └── audit/
│
├── logs/
├── reports/
├── requirements.txt
├── data_dictionary.md
├── design_notes.md
└── README.md

Features

Generates synthetic customer and order data using Faker.
Reads customer and order data from CSV files.
Validates missing values, invalid emails, and duplicate IDs.
Checks relationships between customers and orders.
Masks sensitive customer email addresses.
Separates valid and invalid records.
Maintains audit logs for each pipeline execution.
Performs record count reconciliation.
Measures pipeline execution time.
Includes automated tests using Pytest.

Installation and Setup

1. Create a virtual environment

python -m venv venv

2. Activate the environment (Windows PowerShell)

.\venv\Scripts\Activate.ps1

3. Install the required packages

pip install -r requirements.txt
               
How to Run the Project

Generate sample data:

python -m src.generate_data

This generates 10,000 customer records and 500 order records.

Execute the pipeline:

python -m src.main

Run automated tests:

python -m pytest -q

Output Files

After execution, the pipeline generates:

data/target/analytical_customer.csv – Contains processed customer data.

data/rejects/rejected_records.csv – Contains invalid customer records.

data/rejects/invalid_orders.csv – Contains invalid order records.

data/audit/audit_log.csv – Stores pipeline execution history.

reports/reconciliation_report.txt – Contains record reconciliation results.

Data Privacy

The pipeline protects customer email addresses using masking.

For example:

Original email: sreeja@gmail.com

Masked email: s***@gmail.com

Naming Conventions

Uses lowercase snake_case for file and column names.

Uses customer IDs and order IDs to identify records.

Uses a unique run_id for each pipeline execution.

Uses ISO-8601 format for timestamps.

Uses source_file to track the original input file.