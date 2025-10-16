import os
import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "data")
model_path = os.path.join(script_dir, "model.joblib")
eval_path = os.path.join(script_dir, "metrics.csv")

# Load model
model = load(model_path)

# Load test data
test_data = pd.read_csv(os.path.join(data_path, "validate.csv")) 
y_test = test_data[['species']].values.ravel()
X_test = test_data.drop('species',axis=1)

# Predict
y_pred = model.predict(X_test)

# Compute metrics
metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred, average="weighted"),
    "recall": recall_score(y_test, y_pred, average="weighted"),
    "f1_score": f1_score(y_test, y_pred, average="weighted")
}

# Save metrics to CSV
pd.DataFrame([metrics]).to_csv(eval_path, index=False)