#!/usr/bin/env bash
set -e

PROJECT_ID="winged-quanta-472908-n1"
REGION="us-central1"
REPO="iris-repo"

echo "📦 Deployments:"
kubectl get deployments

echo -e "\n🔹 Services with Model Info:"
for svc in $(kubectl get svc -o jsonpath='{.items[*].metadata.name}'); do
    ext_ip=$(kubectl get svc "$svc" -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || true)
    [ -z "$ext_ip" ] && ext_ip="<pending>"

    pod=$(kubectl get pods -l "app=${svc%-service}" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)
    if [ -n "$pod" ]; then
        model_name=$(kubectl exec "$pod" -- printenv MODEL_NAME 2>/dev/null || echo "-")
        model_ver=$(kubectl exec "$pod" -- printenv MODEL_VERSION 2>/dev/null || echo "-")
        port=$(kubectl exec "$pod" -- printenv IRIS_MODEL_SERVICE_PORT_8200_TCP_PORT 2>/dev/null || echo "-")
    else
        model_name="-"
        model_ver="-"
        port="-"
    fi

    echo "Service: $svc | IP: $ext_ip | Model: $model_name | Version: v$model_ver | Port: $port"
done

echo -e "\n🧩 Pods:"
kubectl get pods

echo -e "\n🗂️ Artifact Registry images:"
gcloud artifacts docker images list "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO"

echo -e "\n🐳 Local Docker images:"
docker images | grep "$REPO" || echo "No local images found."

echo -e "\n✅ Listing complete."
