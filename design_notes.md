# Design Notes and Trade-offs

- CSV and Pandas are used to keep the project simple and easy to run locally without external infrastructure.
- Faker with a fixed seed is used to generate reproducible synthetic customer and order data.
- For duplicate primary keys, the first occurrence is accepted and later occurrences are rejected.
- Email validation checks the email format but does not confirm whether the email address actually exists.
- Customer email addresses are masked after validation. Masking hides part of the email address but is not encryption.
- Valid customer records are published with masked email addresses, while invalid records are stored separately in reject files.
- Publishing uses a temporary file and atomic replacement to avoid partially written output files.
- The pipeline uses an overwrite-based approach, so rerunning it replaces the previous target data instead of appending duplicate records.
- Audit records are appended to preserve the history of pipeline executions.
- The project is designed as a local batch pipeline and does not include cloud processing or distributed systems.
- To process new data, place the updated CSV files in `data/source/` and run the pipeline again.