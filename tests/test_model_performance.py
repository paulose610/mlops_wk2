import os
import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from mlflow.tracking import MlflowClient
import mlflow

mlflow.set_tracking_uri("http://34.133.114.236:8100")
client = MlflowClient(mlflow.get_tracking_uri())

# Global variable
best_model_uri = None


def test_get_best_model():
    global best_model_uri  # ensure it updates for the next test

    model_name = "IRIS-classifier-dt"
    versions = client.search_model_versions(f"name='{model_name}'")

    best_version = None
    best_accuracy = 0

    for v in versions:
        run_id = v.run_id
        run = client.get_run(run_id)
        acc = run.data.metrics.get("accuracy")

        if acc is not None and acc > best_accuracy:
            best_accuracy = acc
            best_version = v

    if best_version:
        print(f"Best model version: {best_version.version}")
        print(f"Run ID: {best_version.run_id}")
        print(f"Accuracy: {best_accuracy}")
        print(f"Stage: {best_version.current_stage}")

        # Correctly store for next test
        best_model_uri = f"models:/{model_name}/{best_version.version}"
        print(f"Best model URI: {best_model_uri}")
    else:
        print("No versions found for this model.")
        assert False, "No registered models found!"


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
