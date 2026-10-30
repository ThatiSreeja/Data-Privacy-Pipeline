"""Safe CSV publishing helpers."""
import os
import tempfile
from pathlib import Path

def save_output(df, output_path):
    """Write to a temporary file, then atomically replace the destination."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=destination.stem + "_",
        suffix=".tmp",
        dir=str(destination.parent)
    )
    os.close(fd)
    try:
        df.to_csv(temporary_name, index=False)
        os.replace(temporary_name, destination)
    except Exception:
        if os.path.exists(temporary_name):
            os.remove(temporary_name)
        raise
