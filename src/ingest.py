"""CSV ingestion helpers."""
import pandas as pd

def load_data(file_path):
    """Load a CSV and attach source lineage columns."""
    df = pd.read_csv(file_path, on_bad_lines="error")
    df["source_file"] = str(file_path)
    # +2 accounts for the CSV header and zero-based DataFrame index.
    df["source_row_number"] = range(2, len(df) + 2)
    return df
