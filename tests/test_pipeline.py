import pandas as pd
from src.publish import save_output

def test_publish_overwrites_safely(tmp_path):
    destination = tmp_path / "nested" / "output.csv"
    save_output(pd.DataFrame({"id": [1]}), destination)
    save_output(pd.DataFrame({"id": [2]}), destination)
    result = pd.read_csv(destination)
    assert result["id"].tolist() == [2]
