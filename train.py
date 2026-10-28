import os
from sklearn.tree import DecisionTreeClassifier
import joblib
from pathlib import Path

# Training data
X = [
    [20, 10000],
    [25, 20000],
    [30, 30000],
    [35, 40000],
    [40, 50000],
    [45, 60000],
]

# 0 = No purchase, 1 = Purchase
y = [0, 0, 0, 1, 1, 1]

# Create model
model = DecisionTreeClassifier(random_state=42)

# Train model
model.fit(X, y)

# Save model to SageMaker model directory
model_dir = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
Path(model_dir).mkdir(parents=True, exist_ok=True)

model_dir = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
Path(model_dir).mkdir(parents=True, exist_ok=True)

model_path = os.path.join(model_dir, "model.joblib")
joblib.dump(model, model_path)

print("Model saved at:", model_path)
print("Model directory files:", os.listdir(model_dir))

print("Model saved at:", model_path)
print("Model directory files:", os.listdir(model_dir))

# Prediction
prediction = model.predict([[38, 45000]])

print("Training completed!")
print("Prediction:", prediction[0])
print("Model saved successfully!")