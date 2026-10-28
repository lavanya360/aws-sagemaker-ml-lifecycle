# aws-sagemaker-ml-lifecycle
End-to-end ML lifecycle using Amazon SageMaker: model training, S3 artifacts, inference code, deployment, and real-time predictions.
# AWS SageMaker ML Lifecycle: Model Training, Deployment & Real-Time Inference

## 1. Project Overview

This project demonstrates an end-to-end Machine Learning (ML) workflow using **Amazon SageMaker and Amazon S3**.

The objective is to understand how a machine learning model moves from training to deployment and how an application can send input data to a deployed model and receive predictions through a real-time inference endpoint.

The project covers the following stages:

1. Prepare a sample dataset.
2. Store model artifacts in Amazon S3.
3. Train a machine learning model using Amazon SageMaker.
4. Package and store the trained model artifacts.
5. Prepare a custom inference script.
6. Create a SageMaker model resource.
7. Configure and deploy a real-time inference endpoint.
8. Send an inference request.
9. Validate the HTTP response and prediction.
10. Understand logging, troubleshooting, and resource cleanup.

This is a learning project designed to demonstrate the fundamental ML lifecycle and the AWS infrastructure involved in deploying a model.

---

## 2. Project Objectives

The main objectives are to:

* Understand the machine learning lifecycle on AWS.
* Learn the difference between model training and model inference.
* Understand how Amazon S3 stores training data and model artifacts.
* Train a scikit-learn model using Amazon SageMaker.
* Understand the role of a SageMaker execution IAM role.
* Package a custom inference script.
* Create a SageMaker model and endpoint configuration.
* Deploy a model for real-time inference.
* Invoke the endpoint and validate its response.
* Understand basic troubleshooting using Amazon CloudWatch Logs.
* Learn why endpoint cleanup is important for cost management.

---

## 3. Architecture

### High-Level Architecture

```text
                 Sample Training Dataset
                           |
                           v
                    Amazon S3
                           |
                           v
                 Amazon SageMaker
                   Training Job
                           |
                           v
                  Trained Model
                  model.tar.gz
                           |
                           v
                    Amazon S3
                  Model Artifacts
                           |
                           v
                SageMaker Model Resource
                           |
                           v
               Endpoint Configuration
                           |
                           v
               SageMaker Real-Time Endpoint
                           |
                           v
                  Inference Request
                           |
                           v
                    Model Prediction
                           |
                           v
                   Inference Response

             Amazon CloudWatch Logs
             Endpoint Troubleshooting
```

### Architecture Explanation

**Amazon S3**

Amazon S3 provides object storage for training data, model artifacts, and supporting project files.

**Amazon SageMaker Training Job**

The training job executes the machine learning training code using the selected training container and compute resources.

**Model Artifact**

After successful training, SageMaker stores the trained model artifacts in Amazon S3. In this project, the artifact is packaged as `model.tar.gz`.

**Inference Script**

The custom `inference.py` script defines how the deployed model is loaded, how incoming requests are processed, how predictions are generated, and how responses are serialized.

**SageMaker Model Resource**

The model resource connects the trained model artifact with the container configuration required for inference.

**Endpoint Configuration**

The endpoint configuration specifies the model to deploy and the compute instance configuration used to serve inference requests.

**SageMaker Endpoint**

The endpoint hosts the model and provides an interface for real-time prediction requests.

**Amazon CloudWatch**

CloudWatch Logs helps investigate endpoint startup problems, container errors, and inference-related issues.

---

## 4. AWS Services and Technologies

| Service or Technology  | Purpose                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| Amazon SageMaker       | Model training and deployment                                       |
| Amazon S3              | Storage for training data and model artifacts                       |
| AWS IAM                | Permissions for SageMaker to access required AWS resources          |
| Amazon ECR             | Container image registry used by the training or inference workflow |
| Amazon CloudWatch Logs | Endpoint logs and troubleshooting                                   |
| Python                 | Training and inference implementation                               |
| scikit-learn           | Machine learning model                                              |
| NumPy                  | Numerical data processing                                           |
| joblib                 | Saving and loading the trained model                                |
| JSON                   | Inference request and response format                               |

**Important:** The exact AWS services involved depend on the training and deployment configuration. For example, the scikit-learn container image used by this project is hosted in Amazon ECR.

---

## 5. Sample Dataset

This project uses a small synthetic dataset for demonstration.

The dataset contains two input features:

* Feature 1: Age-like numeric value
* Feature 2: Income-like numeric value

The target contains binary labels: `0` and `1`.

### Example Training Data

| Feature 1 | Feature 2 | Target |
| --------: | --------: | -----: |
|        20 |     10000 |      0 |
|        25 |     20000 |      0 |
|        30 |     30000 |      0 |
|        35 |     40000 |      1 |
|        40 |     50000 |      1 |
|        45 |     60000 |      1 |

The dataset is intentionally small so that the training and deployment workflow can be understood without needing a large dataset or expensive compute resources.

**Disclaimer:** These are synthetic demonstration values. The features and labels do not represent a validated business rule, and the model must not be used for real-world decisions.

---

## 6. Model Training

A scikit-learn Decision Tree classifier is trained using Amazon SageMaker.

### Training Workflow

1. Prepare the sample dataset.
2. Configure the training environment.
3. Select the scikit-learn training container.
4. Configure the SageMaker execution role.
5. Start the SageMaker training job.
6. Monitor the training job status.
7. Verify that training completes successfully.
8. Locate the resulting model artifact in Amazon S3.

### Training Job

The successful training job created during this project was:

```text
decision-tree-final-20261028043331
```

### Training Container

The training image used was:

```text
720646828776.dkr.ecr.ap-south-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3
```

The image identifies the scikit-learn container used by the training workflow in the Mumbai AWS Region.

### Training Output

The trained model artifact was stored at:

```text
s3://sagemaker-learning-2026-unique123/model-artifacts/decision-tree-final-20261028043331/output/model.tar.gz
```

The archive contains the trained model file used for inference.

---

## 7. Model Artifact and S3

Amazon SageMaker stores the trained model artifact in Amazon S3 so that the deployment process can retrieve it.

### Why Store Model Artifacts in S3?

* To separate model training from model deployment.
* To persist the trained model after the training job finishes.
* To make the artifact available to the model deployment process.
* To support repeatable deployment workflows.
* To avoid retraining the model every time an endpoint is created.

### Important Distinction

**Training job output is not the same as a deployed endpoint.**

A successful training job produces model artifacts. A separate deployment workflow uses those artifacts to create a model resource and an endpoint.

---

## 8. Custom Inference Script

The project uses a custom Python script named:

```text
inference.py
```

The script defines the functions used by the inference container.

### `model_fn`

Loads the trained model from the extracted model artifact directory.

### `input_fn`

Reads the incoming request body and converts the JSON payload into the format expected by the model.

### `predict_fn`

Passes the prepared input to the trained model and generates a prediction.

### `output_fn`

Converts the prediction into a JSON-compatible response.

### Inference Flow

```text
Incoming JSON Request
         |
         v
      input_fn
         |
         v
   Input Validation
   and Preprocessing
         |
         v
      predict_fn
         |
         v
   Trained Model
         |
         v
    Model Prediction
         |
         v
      output_fn
         |
         v
    JSON Response
```

The custom inference script was packaged into:

```text
inference-source-v2.tar.gz
```

The archive was uploaded to Amazon S3 and configured as the inference code source for the SageMaker model resource.

---

## 9. Model Deployment

The deployment workflow uses three important SageMaker resources.

### 9.1 SageMaker Model

The model resource connects the trained model artifact to the container and inference configuration.

Created resource:

```text
decision-tree-model-v4
```

The model configuration references the trained model artifact and the custom inference script.

### 9.2 Endpoint Configuration

The endpoint configuration defines the model and compute resources used to serve predictions.

Created resource:

```text
decision-tree-endpoint-config-v4
```

Configuration used in this project:

| Setting                | Value                    |
| ---------------------- | ------------------------ |
| Production variant     | `AllTraffic`             |
| Model                  | `decision-tree-model-v4` |
| Instance type          | `ml.m5.large`            |
| Initial instance count | `1`                      |

The instance type is part of the endpoint hosting configuration, not the training dataset or model itself.

### 9.3 SageMaker Endpoint

The endpoint hosts the deployed model and accepts real-time inference requests.

Endpoint name:

```text
decision-tree-endpoint-v4
```

The endpoint reached the `InService` state, and a real inference request subsequently returned a successful response.

### Endpoint Lifecycle

```text
Create Model
     |
     v
Create Endpoint Configuration
     |
     v
Create Endpoint
     |
     v
Endpoint Deployment
     |
     v
InService
     |
     v
Invoke Endpoint
     |
     v
Validate Prediction
```

---

## 10. Real-Time Inference

After deployment, the endpoint was invoked with a sample input.

### Input

```json
{
  "instances": [[38, 45000]]
}
```

### Prediction

```json
{
  "predictions": [1]
}
```

### Result

| Property          | Result                      |
| ----------------- | --------------------------- |
| Endpoint          | `decision-tree-endpoint-v4` |
| HTTP status       | `200`                       |
| Sample input      | `[[38, 45000]]`             |
| Prediction        | `[1]`                       |
| Inference request | Successful                  |

The successful request demonstrates that the deployed model can accept input and return a prediction through the SageMaker Runtime API.

**Note:** The prediction is only an output from the demonstration model. It is not evidence of accuracy or suitability for any real-world decision.

---

## 11. Monitoring and Troubleshooting

Amazon CloudWatch Logs can be used to investigate problems during endpoint startup and inference.

The endpoint log group created for this project was:

```text
/aws/sagemaker/Endpoints/decision-tree-endpoint-v4
```

### Useful Troubleshooting Checks

1. Verify the SageMaker training job status.
2. Verify that the model artifact exists in Amazon S3.
3. Verify the IAM role and required permissions.
4. Check the inference script archive structure.
5. Confirm that `inference.py` is at the archive root when required by the selected container configuration.
6. Check that the model loading function can locate the model artifact.
7. Verify the request JSON format.
8. Check the endpoint deployment status.
9. Inspect CloudWatch Logs for container errors.
10. Invoke the endpoint and verify the HTTP response.

### Example Issue Encountered

An earlier inference package contained notebook JSON instead of a valid Python inference script.

This caused an error involving:

```text
NameError: name 'null' is not defined
```

The cause was that notebook metadata such as `"execution_count": null` had been included in a file being executed as Python.

### Resolution

The inference source was corrected, packaged into a new archive, uploaded to S3, and configured in a new SageMaker model resource.

The new endpoint was successfully deployed and tested.

### Lesson Learned

A file named `inference.py` must contain valid Python code. Renaming a Jupyter Notebook JSON file to `inference.py` does not convert it into a Python script.

---

## 12. IAM and Security Considerations

The SageMaker execution role used in this project was:

```text
SageMakerLearningExecutionRole
```

The role allows SageMaker to access the AWS resources required by the configured workflow, subject to its attached permissions.

### Security Best Practices

* Apply least-privilege IAM permissions.
* Avoid using broad permissions such as unrestricted administrative access for routine ML workloads.
* Keep AWS access keys and secrets out of source code.
* Do not upload credentials, tokens, or `.env` files to GitHub.
* Avoid publishing sensitive AWS account details in a public repository.
* Keep S3 buckets private unless public access is explicitly required.
* Review CloudWatch logs before publishing them.
* Use placeholders in public documentation for account-specific resource names.

The role ARN, bucket name, and other AWS resource identifiers should be reviewed before making the repository public.

---

## 13. Cost Management and Cleanup

SageMaker training and endpoint hosting have different cost characteristics.

### Training Costs

A training job uses the configured training compute resources while it runs. Once the training job completes, its training instances are not intended to remain running as an always-on endpoint.

### Endpoint Hosting Costs

A real-time endpoint provisions hosting compute resources. These resources can continue to incur charges while the endpoint remains deployed, even when it receives no inference requests.

### Cleanup Checklist

After completing testing:

1. Save the code and required project documentation.
2. Save any model artifacts that you intentionally want to retain.
3. Delete the SageMaker endpoint when it is no longer needed.
4. Delete the endpoint configuration if it is no longer required.
5. Delete the SageMaker model resource if it is no longer required.
6. Review S3 objects and remove unnecessary artifacts.
7. Check AWS billing and Cost Explorer for charges.

**Important:** Deleting the endpoint does not automatically delete every related resource or every S3 object. Review each resource separately.

Do not delete the S3 model artifact if you still need it for future redeployment.

---

## 14. Repository Structure

The following is the proposed GitHub repository structure. Only add files that you have actually created and verified.

```text
aws-sagemaker-ml-lifecycle/
│
├── README.md
│
├── training/
│   └── train.py
│
├── inference/
│   └── inference.py
│
├── deployment/
│   └── deployment-notes.md
│
├── tests/
│   └── test_inference.py
│
├── architecture/
│   └── architecture.md
│
└── .gitignore
```

### File Responsibilities

* `README.md`: Project overview, architecture, setup, results, and cleanup.
* `training/train.py`: Training code, if extracted and verified.
* `inference/inference.py`: Custom model loading and inference functions.
* `deployment/deployment-notes.md`: Deployment steps and resource configuration.
* `tests/test_inference.py`: Inference unit tests, if implemented.
* `architecture/architecture.md`: Architecture notes or diagrams.
* `.gitignore`: Excludes credentials, temporary files, and generated artifacts that should not be committed.

This structure is a recommendation; it does not imply that all these files have already been created.

---

## 15. Key Learnings

By completing this project, I practiced the following concepts:

* Amazon SageMaker training jobs.
* Training container configuration.
* Amazon S3 model artifact storage.
* SageMaker model resources.
* Custom inference scripts.
* Endpoint configurations.
* Real-time inference endpoints.
* SageMaker Runtime API invocation.
* JSON-based inference requests and responses.
* CloudWatch Logs for troubleshooting.
* IAM execution roles.
* Endpoint lifecycle management.
* AWS resource cleanup and cost awareness.

The project helped connect machine learning concepts with cloud infrastructure and model-serving operations.

---

## 16. Future Improvements

Potential next steps include:

* Add a reproducible training script.
* Add input validation and clearer error handling.
* Add unit tests for model loading and prediction.
* Compare different model types and evaluation metrics.
* Add model evaluation before deployment.
* Add batch inference using an appropriate SageMaker workflow.
* Add endpoint monitoring and alarms.
* Explore autoscaling for inference endpoints.
* Automate deployment using infrastructure as code.
* Introduce a CI/CD pipeline for model deployment.
* Explore model registry and model versioning.
* Evaluate deployment options for production workloads.

These are future improvements, not features claimed as completed in the current project.

---

## 17. Conclusion

This project demonstrates a basic end-to-end machine learning deployment workflow using Amazon SageMaker and Amazon S3.

A scikit-learn Decision Tree model was trained, its artifact was stored in S3, a custom inference script was configured, and the model was deployed to a SageMaker real-time endpoint. A test inference request returned HTTP status `200` and prediction `[1]`.

The project provides a foundation for further learning in MLOps, model serving, monitoring, security, automation, and AI infrastructure engineering.

---

## Disclaimer

This repository is intended for educational purposes. The dataset and predictions are synthetic demonstrations. AWS resource availability, service configuration, and pricing can vary by Region and over time. Review the current AWS pricing and delete unused resources to avoid unnecessary charges.
