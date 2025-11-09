import os
import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from mlflow.tracking import MlflowClient
import mlflow

mlflow.set_tracking_uri("http://136.112.91.129:8100")
client = MlflowClient(mlflow.get_tracking_uri())

# Global variable
best_model_uri = None


def test_get_latest_model():
    global best_model_uri  # keep name same if other tests depend on it

    model_name = "IRIS-classifier-dt"
    versions = client.search_model_versions(f"name='{model_name}'")

    if not versions:
        print("No versions found for this model.")
        assert False, "No registered models found!"

    # Get the latest version (highest version number)
    latest_version = max(versions, key=lambda v: int(v.version))

    print(f"Latest model version: {latest_version.version}")
    print(f"Run ID: {latest_version.run_id}")
    print(f"Stage: {latest_version.current_stage}")

    best_model_uri = f"models:/{model_name}/{latest_version.version}"
    print(f"Latest model URI: {best_model_uri}")



def test_model_performance():
    global best_model_uri
    assert best_model_uri, "best_model_uri not set — run test_get_best_model() first!"

    # Paths
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(script_dir, "data", "validate.csv")
    metrics_path = os.path.join(script_dir, "metadata", "metrics.csv")

    # Load model from MLflow Registry
    model = mlflow.sklearn.load_model(best_model_uri)
    print("Model loaded from registry successfully!")

    # Load test data
    df = pd.read_csv(data_path)
    y_test = df["species"].values
    X_test = df.drop("species", axis=1)

    # Evaluate
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted"),
        "recall": recall_score(y_test, y_pred, average="weighted"),
        "f1_score": f1_score(y_test, y_pred, average="weighted"),
    }

    # Save metrics for report
    pd.DataFrame([metrics]).to_csv(metrics_path, index=False)
    print("Metrics saved successfully:", metrics)

if __name__ == "__main__":
    test_get_latest_model()
    test_model_performance()