import mlflow
import subprocess

# --- Configuration ---
MLFLOW_TRACKING_URI = "http://35.184.91.21:8100"
MODEL_NAME = "IRIS-classifier-dt"
IMAGE_BASE = "us-central1-docker.pkg.dev/winged-quanta-472908-n1/iris-repo/iris-model"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# --- 1. Get latest model version ---
client = mlflow.tracking.MlflowClient()
versions = client.search_model_versions(f"name='{MODEL_NAME}'")
latest_version = max(versions, key=lambda v: int(v.version)).version
print(f"Latest model version: {latest_version}")

# --- 2. Build & push Docker image ---
tag = f"{IMAGE_BASE}:v{latest_version}"
subprocess.run([
    "docker", "build",
    "-t", tag,
    "--build-arg", f"MODEL_NAME={MODEL_NAME}",
    "--build-arg", f"MODEL_VERSION={latest_version}",
    "."
], check=True)

subprocess.run(["docker", "push", tag], check=True)

# --- 3. Deploy Kubernetes manifests ---
for manifest in ["deployment.yaml", "service.yaml", "hpa.yaml"]:
    print(f"Applying {manifest} ...")
    subprocess.run(
        f"env MODEL_NAME={MODEL_NAME} MODEL_VERSION={latest_version} envsubst < {manifest} | kubectl apply -f -",
        shell=True,
        check=True
    )

print(f"\n✅ Deployed model '{MODEL_NAME}' version {latest_version} with image tag v{latest_version}")
print("✅ Deployment, Service, and HPA applied successfully.")
