# Week 7 → Model Deployment + Monitoring and Stress Testing(Kubernetes + FastAPI)

## Helper Scripts

- **cleanup.sh**  
  Cleans up existing Kubernetes deployments, services, and pods to ensure a fresh environment before redeployment.

- **show_live.sh**  
  Displays the current live status of all Kubernetes components — including deployments, services, pods, and container registry details.

## Utility Files

- **cd.yaml**  
  Continuous Deployment configuration file used in the CI/CD pipeline for automated model rollout + stress testing at the end of deployment.

- **deploy_latest.py**  
  Python script that updates Kubernetes manifests and triggers deployment for the latest model version.

- **deployment.yaml**  
  Kubernetes manifest for deploying the model-serving FastAPI application (container image, replicas, and metadata) + new monitoring code.

- **service.yaml**  
  Kubernetes manifest defining a LoadBalancer service to expose the model’s API externally.

- **Dockerfile**  
  Builds the container image that serves the ML model through FastAPI.

- **model_server.py**  
  FastAPI application responsible for loading the trained model and serving inference requests + added monitoring code for week 7 with new endpoints for monitoring.

- **post.lua**
  file for stress testing.
