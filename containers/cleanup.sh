#!/usr/bin/env bash
set -e

PROJECT_ID="winged-quanta-472908-n1"
REGION="us-central1"
REPO="iris-repo"
IMAGE="iris-model"

echo "🧹 Deleting Kubernetes deployments and services..."
kubectl get deployments -o name | grep iris-model | xargs -r kubectl delete --ignore-not-found
kubectl get svc -o name | grep iris-model | xargs -r kubectl delete --ignore-not-found

echo "🧹 Deleting all images from Artifact Registry..."
gcloud artifacts docker images list $REGION-docker.pkg.dev/$PROJECT_ID/$REPO \
  --format="get(package)" | while read -r image; do
    gcloud artifacts docker images delete "$image" --delete-tags --quiet || true
done

echo "🧹 Deleting local Docker images tagged 'v<number>'..."
docker images "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE" \
  --format "{{.Repository}}:{{.Tag}}" | grep -E ":v[0-9]+" | while read -r tag; do
    docker rmi -f "$tag" || true
done

echo "✅ Cleanup complete."

