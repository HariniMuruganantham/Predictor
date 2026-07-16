# Kubernetes Diagnostic Notes – Deliberate Breakage Exercise

<p align="center">

![Kubernetes](https://img.shields.io/badge/Kubernetes-Troubleshooting-326CE5?style=for-the-badge\&logo=kubernetes\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge\&logo=docker\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-000000?style=for-the-badge\&logo=flask\&logoColor=white)
![Status](https://img.shields.io/badge/Lab-Completed-success?style=for-the-badge)

</p>

---

## Objective

This exercise intentionally introduced failures into a Kubernetes-deployed Flask application to practice diagnosing and resolving common deployment issues using Kubernetes troubleshooting commands.

---

# Break 1 – Invalid Image Tag

## Change Introduced

Updated the deployment image from:

```yaml
image: predictor:v0.2
```

to:

```yaml
image: predictor:v9.9
```

---

## Observed Symptom

The pod failed to start and entered the following state:

```text
ErrImageNeverPull
```

---

## First Command That Revealed the Root Cause

```bash
kubectl describe pod <pod-name>
```

---

## Root Cause

The deployment referenced a Docker image tag that did not exist locally.

Since the deployment was configured with:

```yaml
imagePullPolicy: Never
```

Kubernetes did not attempt to pull the image from a registry and failed because the image was unavailable.

---

## Resolution

Restored the deployment image:

```yaml
image: predictor:v0.2
```

Applied the updated deployment:

```bash
kubectl apply -f k8s/deployment.yaml
```

---

## Verification

```bash
kubectl get pods
```

The pod successfully returned to the `Running` state.

---

# Break 2 – Application Startup Failure

## Change Introduced

Introduced an intentional Python syntax error in `app.py`.

Example:

```python
print("Starting"
```

---

## Observed Symptom

The application container continuously restarted.

Pod status:

```text
CrashLoopBackOff
```

---

## First Command That Revealed the Root Cause

```bash
kubectl logs <pod-name> --previous
```

---

## Root Cause

The Flask application failed to start because of a Python syntax error.

Observed log:

```text
SyntaxError: '(' was never closed
```

---

## Resolution

Removed the intentional syntax error.

Rebuilt the Docker image:

```bash
docker build -t predictor:v0.2 .
```

Restarted the deployment:

```bash
kubectl rollout restart deployment predictor
```

---

## Verification

```bash
kubectl get pods
```

The pod returned to the `Running` state successfully.

---

# Break 3 – Service Port Mismatch

## Change Introduced

Modified the Kubernetes Service configuration:

```yaml
targetPort: 5000
```

to:

```yaml
targetPort: 9999
```

---

## Observed Symptom

The application pod remained healthy, but the Service could not correctly route traffic to the application.

---

## First Command That Revealed the Root Cause

```bash
kubectl describe svc predictor-svc
```

---

## Root Cause

The Service was forwarding requests to port `9999`, while the Flask application was listening on port `5000`.

Observed output:

```text
TargetPort: 9999/TCP
Endpoints: 10.xxx.xxx.xxx:9999
```

---

## Resolution

Restored the correct Service configuration:

```yaml
targetPort: 5000
```

Applied the updated Service:

```bash
kubectl apply -f k8s/service.yaml
```

---

## Verification

```bash
kubectl describe svc predictor-svc
```

Confirmed output:

```text
TargetPort: 5000/TCP
Endpoints: 10.xxx.xxx.xxx:5000
```

---

# Troubleshooting Summary

| Break                       | Symptom             | First Diagnostic Command             | Root Cause                                  | Resolution                                                         |
| --------------------------- | ------------------- | ------------------------------------ | ------------------------------------------- | ------------------------------------------------------------------ |
| Invalid Image Tag           | `ErrImageNeverPull` | `kubectl describe pod`               | Invalid Docker image tag (`predictor:v9.9`) | Restored image to `predictor:v0.2`                                 |
| Application Startup Failure | `CrashLoopBackOff`  | `kubectl logs --previous`            | Python syntax error                         | Removed the error, rebuilt the image, and restarted the deployment |
| Service Port Mismatch       | Service unreachable | `kubectl describe svc predictor-svc` | Incorrect `targetPort`                      | Restored `targetPort: 5000`                                        |

---

# Final Validation

After restoring all configurations:

```bash
kubectl get pods
kubectl get svc
```

Result:

* Deployment healthy
* Pod running
* Service routing traffic correctly
* All API endpoints accessible

Health check response:

```json
{
  "status": "ok"
}
```

---

# Key Learning Outcomes

* Diagnosed image-related deployment failures using `kubectl describe pod`.
* Identified application startup failures using `kubectl logs --previous`.
* Investigated Kubernetes Service configuration issues using `kubectl describe svc`.
* Restored deployments and validated application health after each fix using Kubernetes diagnostic commands.
