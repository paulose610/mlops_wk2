import os
import pandas as pd

def test_data_shape_and_columns():
    # Path setup
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(script_dir, "data", "validate.csv")

    # Load data
    df = pd.read_csv(data_path)

    # Expected columns
    expected_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]

    # Validate columns
    assert all(col in df.columns for col in expected_columns), f"Missing columns: {set(expected_columns) - set(df.columns)}"

    # Validate non-empty and reasonable shape
    assert len(df) > 0, "Validation dataset is empty"
    assert df.shape[1] == len(expected_columns), "Unexpected number of columns"
