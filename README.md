# GKE Sample App 🚀

This is a simple **Node.js + Express app** deployed on **Google Kubernetes Engine (GKE)** using:

- GitHub → Jenkins → Artifact Registry → GKE

## How it Works
1. Developer pushes code to GitHub.
2. Jenkins builds Docker image and pushes it to Artifact Registry.
3. Jenkins updates the Kubernetes Deployment in GKE.
4. Service exposes the app via LoadBalancer.

## Deploy Manually First
```bash
kubectl apply -f k8s/
kubectl get svc gke-app-service
