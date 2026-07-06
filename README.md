 Predictor — CI/CD Pipeline Health Predictor (v0.1)

A small Flask API that serves simulated CI/CD pipeline run data, containerized
with Docker and deployed to Kubernetes (minikube). Built to eventually predict
deploy failure risk before shipping — inspired by real CI/CD pain at Inflow
(the Docker layer-cache bug, TASK-037 tag-verification insight).

## Endpoints
- `GET /health` — liveness check, returns `{"status": "ok"}`
- `GET /pipelines` — 10 simulated pipeline runs
- `GET /pipelines/failed` — only the failed runs from a batch of 20
- `GET /config` — returns the current LOG_LEVEL, read from the K8s ConfigMap

## Running locally
```
pip install -r requirements.txt
python app.py
curl http://localhost:5000/health
```

## Running in Docker
```
docker build -t predictor:v0.1 .
docker run -p 5000:5000 predictor:v0.1
curl http://localhost:5000/health
```

## Deploying to Kubernetes (minikube)
```
eval $(minikube docker-env)
docker build -t predictor:v0.1 .
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service predictor-svc --url
```

## Architecture
- **Deployment**: 1 replica, reads `LOG_LEVEL` from a ConfigMap as an env var
- **Service**: NodePort, exposes port 5000 externally on minikube for local testing
- **ConfigMap**: holds non-sensitive runtime config (`LOG_LEVEL`, `APP_ENV`)
