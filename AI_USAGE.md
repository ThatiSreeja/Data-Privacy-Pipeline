# AI Usage and Transparency

## AI Tools Used

I used ChatGPT as an AI assistant during the development of this Python Data Privacy Pipeline project.

## Where AI Accelerated My Work

ChatGPT helped me understand the assignment requirements and organize the project into separate Python modules. It also helped me understand concepts such as data validation, duplicate detection, referential integrity, email masking, audit logging, and data reconciliation.

AI assistance helped me identify implementation approaches, understand Python code, troubleshoot errors, and prepare project documentation.

## Where I Relied Heavily on AI

I relied on ChatGPT for guidance on:
- Designing the project folder structure and workflow.
- Understanding and implementing customer and order validation.
- Handling invalid records and duplicate IDs.
- Implementing email masking.
- Creating audit logs and reconciliation checks.
- Understanding pytest and writing test cases.
- Debugging errors and preparing README and design documentation.

I used AI-generated suggestions as implementation guidance and reviewed the code to understand how the different modules work together.

## What I Personally Reviewed, Changed, and Validated

I personally:
- Reviewed the project structure and Python files.
- Clarified that the privacy transformation used in my pipeline is email masking.
- Installed the project dependencies in a local virtual environment.
- Generated 10,000 customer records and 500 order records.
- Executed the main pipeline locally.
- Checked the execution output and reconciliation results.
- Verified that customer records were divided into 9,839 valid records and 161 rejected records.
- Verified that order records were divided into 483 valid records and 17 rejected records.

Both customer and order reconciliation checks passed during my execution.

## Testing Status

The data generation and main pipeline execution completed successfully. However, pytest encountered an internal environment error before the test results could be confirmed. Therefore, I am not claiming that the automated test suite passed.

## Limitations

- The project uses local CSV files and Pandas.
- Email masking hides part of an email address; it is not encryption.
- Email format validation does not verify whether an email address actually exists.
- The project does not use cloud infrastructure or distributed processing.

## Declaration

ChatGPT was used as an assistance tool for learning, implementation guidance, debugging, and documentation. I am responsible for reviewing and understanding the submitted project and its implementation. I have documented the execution and testing status based on what I actually verified.