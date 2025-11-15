# Week 8 modifications only on mlflow_train.ipynb (Did not create a new branch--done on exp branch)
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


# Stress Test Results Summary

## Test 1 — 2000 Concurrent Connections
Running 5m test @ http://35.193.193.246:80/predict
Threads: 4, Connections: 2000

- Average Latency: 1.27s
- Std Dev: 456.90ms
- Max Latency: 2.80s
- Requests per Second: 51.43
- Total Requests: 22,637 in 5.00m
- Socket Errors: connect 0, read 8236, write 6762377, timeout 11615
- Transfer/sec: 16.87KB

---

## Test 2 — 1000 Concurrent Connections
Running 5m test @ http://35.193.193.246:80/predict
Threads: 4, Connections: 1000

- Average Latency: 1.25s
- Std Dev: 468.07ms
- Max Latency: 2.08s
- Requests per Second: 61.60
- Total Requests: 42,059 in 5.00m
- Socket Errors: connect 0, read 6326, write 1734, timeout 118
- Transfer/sec: 31.55KB
