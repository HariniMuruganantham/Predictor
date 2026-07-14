# Predictor — CI/CD Pipeline Health Predictor

![version](https://img.shields.io/github/v/tag/HariniMuruganantham/Predictor?label=version&sort=semver)
![last commit](https://img.shields.io/github/last-commit/HariniMuruganantham/Predictor)
![python](https://img.shields.io/badge/python-3.x-blue?logo=python&logoColor=white)
![flask](https://img.shields.io/badge/flask-API-black?logo=flask&logoColor=white)
![docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white)
![kubernetes](https://img.shields.io/badge/kubernetes-minikube-326CE5?logo=kubernetes&logoColor=white)

A Flask API that serves simulated CI/CD pipeline run data, containerized with Docker and deployed to Kubernetes (minikube). Built to eventually predict deploy failure risk before shipping, inspired by real CI/CD issues encountered at Inflow (a Docker layer-cache bug, and a tag-verification insight from TASK-037).

## Current version: v0.2

See [Version History](#version-history) below for what changed between releases.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness check, returns `{"status": "ok"}` |
| GET | `/pipelines` | Returns 10 simulated pipeline runs |
| GET | `/pipelines/failed` | Returns only the failed runs from a batch of 20 |
| GET | `/config` | Returns the current `LOG_LEVEL`, read from the Kubernetes ConfigMap |

## Running locally

```bash
pip install -r requirements.txt
python app.py
curl http://localhost:5000/health
```

## Running in Docker

```bash
docker build -t predictor:v0.2 .
docker run -p 5000:5000 predictor:v0.2
curl http://localhost:5000/health
```

## Deploying to Kubernetes (minikube)

```bash
eval $(minikube docker-env)
docker build -t predictor:v0.2 .
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service predictor-svc --url
```

## Architecture

- **Deployment**: 1 replica, reads `LOG_LEVEL` from a ConfigMap as an environment variable. Configured with CPU/memory resource requests and limits, plus liveness and readiness probes against `/health`.
- **Service**: NodePort, exposes port 5000 externally on minikube for local testing.
- **ConfigMap**: holds non-sensitive runtime configuration (`LOG_LEVEL`, `APP_ENV`).
