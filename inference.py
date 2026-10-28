```python
import os
import json
import joblib
import numpy as np


def model_fn(model_dir):
    """
    Load the trained model from the model artifact directory.
    SageMaker calls this function when the inference container starts.
    """
    model_path = os.path.join(model_dir, "model.joblib")
    model = joblib.load(model_path)
    return model


def input_fn(request_body, request_content_type):
    """
    Parse the incoming JSON request and convert it into a NumPy array.
    Expected request:
    {
        "instances": [[38, 45000]]
    }
    """
    if request_content_type != "application/json":
        raise ValueError(
            f"Unsupported content type: {request_content_type}"
        )

    data = json.loads(request_body)
    instances = data["instances"]

    return np.asarray(instances)


def predict_fn(input_data, model):
    """
    Generate predictions using the loaded scikit-learn model.
    """
    predictions = model.predict(input_data)
    return predictions


def output_fn(prediction, accept):
    """
    Convert model predictions into a JSON response.
    """
    if accept != "application/json":
        raise ValueError(f"Unsupported accept type: {accept}")

    response = {
        "predictions": prediction.tolist()
    }

    return json.dumps(response), "application/json"
```
