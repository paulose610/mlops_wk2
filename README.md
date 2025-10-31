# Week 6 → Model Deployment (Kubernetes + FastAPI)

## Github Link
Repository: [paulose610/mlops_wk2 (dev branch)](https://github.com/paulose610/mlops_wk2/tree/dev)

## Helper Scripts

- **cleanup.sh**  
  Cleans up existing Kubernetes deployments, services, and pods to ensure a fresh environment before redeployment.

- **show_live.sh**  
  Displays the current live status of all Kubernetes components — including deployments, services, pods, and container registry details.

## Utility Files

- **cd.yaml**  
  Continuous Deployment configuration file used in the CI/CD pipeline for automated model rollout.

- **deploy_latest.py**  
  Python script that updates Kubernetes manifests and triggers deployment for the latest model version.

- **deployment.yaml**  
  Kubernetes manifest for deploying the model-serving FastAPI application (container image, replicas, and metadata).

- **service.yaml**  
  Kubernetes manifest defining a LoadBalancer service to expose the model’s API externally.

- **Dockerfile**  
  Builds the container image that serves the ML model through FastAPI.

- **model_server.py**  
  FastAPI application responsible for loading the trained model and serving inference requests.
