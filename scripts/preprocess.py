import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Path to your CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "../data")
# Load the dataset
df = pd.read_csv(data_path)

# Assuming the last column is the target
X = df.iloc[:, :-1]  # all columns except last
y = df.iloc[:, -1]   # last column

# Split into train and test sets (e.g., 80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify = y)

# Save the splits as CSV
X_train.to_csv("data/X_train.csv", index=False)
X_test.to_csv("data/X_test.csv", index=False)
y_train.to_csv("data/y_train.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)

# Delete the original data.csv
os.remove(data_path)

print("Train/test split created and original data.csv deleted.")

