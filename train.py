import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
from datetime import datetime
import os

# Load the data
data_path = "data"  # Adjust if your CSVs are in a different folder
X_train = pd.read_csv(os.path.join(data_path, "X_train.csv"))
X_test = pd.read_csv(os.path.join(data_path, "X_test.csv"))
y_train = pd.read_csv(os.path.join(data_path, "y_train.csv")).values.ravel()  # flatten
y_test = pd.read_csv(os.path.join(data_path, "y_test.csv")).values.ravel()

# Initialize the Decision Tree classifier with some simple hyperparameters
clf = DecisionTreeClassifier(max_depth=1, min_samples_split=10, random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy on train set: {acc:.4f}")

# Save the model using joblib
model_file = "model.joblib"
joblib.dump(clf, model_file)

# Print timestamp
print(f"Model saved as '{model_file}' at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
