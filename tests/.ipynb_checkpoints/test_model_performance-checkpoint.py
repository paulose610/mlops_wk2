import os
import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def test_model_performance():
    # Paths
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(script_dir, "data", "validate.csv")
    model_path = os.path.join(script_dir, "model.joblib")
    metrics_path = os.path.join(script_dir, "metrics.csv")

    # Load model + data
    model = load(model_path)
    df = pd.read_csv(data_path)

    y_test = df['species'].values
    X_test = df.drop('species', axis=1)

    # Predict
    y_pred = model.predict(X_test)

    # Compute metrics
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted"),
        "recall": recall_score(y_test, y_pred, average="weighted"),
        "f1_score": f1_score(y_test, y_pred, average="weighted")
    }

    # Save metrics (used in report)
    pd.DataFrame([metrics]).to_csv(metrics_path, index=False)
