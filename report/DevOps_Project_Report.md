# DEVOPS COURSE PROJECT REPORT

**Course Code:** 25CIAEC59 / 25CYAEC59  
**Course Title:** DevOps  
**Total Marks:** 20 (Component 1: 10 Marks | Component 2: 10 Marks)  

---

## PROJECT TITLE:
### Automated End-to-End CI/CD Pipeline and Cloud-Native Kubernetes Orchestration for Campus Lab Resources Management

---

### STUDENT DETAILS:
- **Student Name:** [Enter Your Name Here]
- **USN / Roll Number:** [Enter Your USN/ID Here]
- **Branch / Semester:** Computer Science & Engineering / [Your Semester]
- **GitHub Repository Link:** `https://github.com/<YOUR_USERNAME>/campus-lab-devops-pipeline`

---

## CERTIFICATE

This is to certify that the project work entitled **"Automated End-to-End CI/CD Pipeline and Cloud-Native Kubernetes Orchestration for Campus Lab Resources Management"** is a bona fide record of work carried out by **[Student Name]** bearing USN **[Your USN]** in partial fulfillment of the requirements for the course **DevOps (Course Code: 25CIAEC59 / 25CYAEC59)**.

\
**Faculty In-Charge / Evaluator:** ________________________  
**Date:** ________________________  

---
\pagebreak

# COMPONENT 1: CI/CD Pipeline with Git, Build Automation & Jenkins (10 Marks)

## 1. Abstract
Component 1 focuses on the implementation of a Continuous Integration (CI) pipeline for a Campus Lab Resources Management microservice. The application is maintained under Git version control using structured branching and merge workflows. The automated pipeline is established using Jenkins and GitHub Actions to automatically detect code changes, execute unit test suites, package release artifacts, and archive build outputs on every commit. This eliminates manual build overhead, guarantees software stability, and shortens release feedback cycles.

## 2. Introduction
In educational institutions, campus laboratories manage high-value, specialized resources including AI GPU workstations, 3D printers, digital storage oscilloscopes, Cisco network racks, and robotics equipment. Efficient scheduling and inventory tracking are critical. To deliver updates rapidly without introducing regressions, modern DevOps practices mandate continuous integration. 

Component 1 establishes an automated assembly line that tracks code versions, executes automated tests prior to packaging, and produces verified distribution artifacts upon every developer push.

## 3. Implementation

### 3.1 Development Environment
- **Operating System:** Windows 11 / Linux Subsystem
- **Programming Language & Framework:** Python 3.12, Flask 3.0.3
- **Testing Framework:** pytest 8.2.0, unittest
- **Version Control:** Git 2.40+ & GitHub
- **Continuous Integration Server:** Jenkins LTS 2.440+ & GitHub Actions
- **Packaging Utility:** Python tarfile packaging module

### 3.2 Application Architecture and Code
The Campus Lab Resources Management API provides an in-memory repository of laboratory assets with CRUD capabilities.

#### Key Endpoints:
- `GET /`: Returns API discovery metadata and active campus identification.
- `GET /health`: Returns service health (`{"status": "UP"}`), environment, and inventory count.
- `GET /api/resources`: Returns list of all lab resources with query parameters (`status`, `lab`).
- `GET /api/resources/<id>`: Returns details for an individual equipment asset.
- `POST /api/resources`: Registers new laboratory equipment or records student allocations.

#### Core Application Code (`src/app.py`):
```python
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
APP_PORT = int(os.environ.get("APP_PORT", 5000))
APP_ENV = os.environ.get("APP_ENV", "development")

RESOURCES = [
    {"id": 1, "name": "NVIDIA RTX 4090 Workstation", "lab": "AI & Deep Learning Lab", "type": "Compute", "status": "Available", "allocated_to": None},
    {"id": 2, "name": "Ultimaker S5 3D Printer", "lab": "Prototyping & Robotics Lab", "type": "Hardware", "status": "In-Use", "allocated_to": "Student-21BCS104"},
    {"id": 3, "name": "Keysight Digital Storage Oscilloscope", "lab": "VLSI Lab", "type": "Testing Equipment", "status": "Available", "allocated_to": None},
    {"id": 4, "name": "Cisco Catalyst 9300 Switch Rack", "lab": "Advanced Networks Lab", "type": "Networking", "status": "Maintenance", "allocated_to": None}
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP", "service": "campus-lab-resources-api", "environment": APP_ENV, "total_resources": len(RESOURCES)}), 200

@app.route("/api/resources", methods=["GET"])
def get_resources():
    status_filter = request.args.get("status")
    results = RESOURCES
    if status_filter:
        results = [r for r in results if r["status"].lower() == status_filter.lower()]
    return jsonify({"count": len(results), "resources": results}), 200

@app.route("/api/resources", methods=["POST"])
def create_resource():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("lab"):
        return jsonify({"error": "Missing mandatory fields"}), 400
    new_id = max([r["id"] for r in RESOURCES], default=0) + 1
    new_resource = {"id": new_id, "name": data.get("name"), "lab": data.get("lab"), "type": data.get("type", "General"), "status": data.get("status", "Available"), "allocated_to": data.get("allocated_to", None)}
    RESOURCES.append(new_resource)
    return jsonify({"message": "Resource registered successfully", "resource": new_resource}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)
```

### 3.3 Git Version Control & Branching Strategy
The project repository was initialized with a `main` branch. A dedicated feature branch (`feature/lab-endpoints`) was created to develop lab query and booking enhancements. Once verified, the branch was merged into `main` using a non-fast-forward merge (`git merge --no-ff`), preserving the branch topology in history.

```bash
git init -b main
git add .
git commit -m "feat: initial commit with campus lab resource management core structure"
git checkout -b feature/lab-endpoints
# [Perform code additions and tests]
git commit -am "feat: add lab equipment search filter and booking validation enhancement"
git checkout main
git merge --no-ff feature/lab-endpoints -m "Merge branch 'feature/lab-endpoints' into main"
```

### 3.4 Build and Packaging Configuration
The build script (`package.py`) validates dependencies and packages the source files into a timestamped release archive `dist/campus-lab-api-1.0.0.tar.gz`.

### 3.5 Jenkins CI Pipeline Configuration
The declarative `Jenkinsfile` configures an automated pipeline triggered via SCM polling (`pollSCM('H/2 * * * *')`). The pipeline executes:
1. **Checkout Code:** Retrieves latest commit from GitHub repository.
2. **Run Unit Tests:** Executes test cases with pytest.
3. **Build & Package Artifact:** Packages source files into `dist/*.tar.gz`.
4. **Post-Build Action:** Automatically archives build artifacts (`archiveArtifacts artifacts: 'dist/*.tar.gz'`).

---

## 4. Chosen CI Enhancements and Justification

### Selected Enhancements:
1. **Automated Unit Tests in CI Pipeline:**  
   *Justification:* Shipping untested code into production causes unexpected service outages. Adding an automated test phase before packaging ensures that all 4 critical test cases (health endpoint, inventory listing, ID lookup, and validation logic) pass. If any test fails, Jenkins terminates the build immediately, preventing corrupted releases.
2. **GitHub Actions alongside Jenkins (`.github/workflows/ci.yml`):**  
   *Justification:* Demonstrates multi-tool CI orchestration. While Jenkins runs on internal on-premises servers, GitHub Actions provides distributed cloud-based CI execution for rapid pull-request checks and immediate status badges on GitHub.

---

## 5. Results & Evidence (Component 1 Screenshots)

### 5.1 Screenshot 1: Git Branch and Commit History
*Description: Terminal output showing `git log --graph --oneline --all` displaying the feature branch and merge commit.*
```text
[PASTE SCREENSHOT HERE: Terminal showing git log --graph showing feature/lab-endpoints merged into main]
```

### 5.2 Screenshot 2: Jenkins Job Configuration
*Description: Jenkins UI showing Source Code Management pointing to Git repository, Poll SCM trigger, and Pipeline script path.*
```text
[PASTE SCREENSHOT HERE: Jenkins Pipeline Configuration page showing Git SCM and Poll SCM trigger]
```

### 5.3 Screenshot 3: Successful Jenkins Build Console Output
*Description: Console log demonstrating successful checkout, test pass, packaging, and FINISHED: SUCCESS with green status.*
```text
[PASTE SCREENSHOT HERE: Jenkins Console Output showing SUCCESS]
```

### 5.4 Screenshot 4: Archived Build Artifact
*Description: Jenkins build summary page displaying the archived artifact `campus-lab-api-1.0.0.tar.gz`.*
```text
[PASTE SCREENSHOT HERE: Jenkins UI showing Last Successful Artifacts]
```

### 5.5 Screenshot 5: CI Enhancement Evidence (Test Results / GitHub Actions)
*Description: GitHub Actions tab showing green checkmarks on Build, Test & Package job.*
```text
[PASTE SCREENSHOT HERE: GitHub Actions workflow run passing all stages]
```

---

## 6. Conclusion (Component 1)
Component 1 established an automated continuous integration pipeline for the Campus Lab Resources Management microservice. Git version control with branch isolation guarantees clean history, while Jenkins and GitHub Actions ensure automated verification and repeatable artifact delivery.

---

## 7. References (Component 1)
1. Jenkins Declarative Pipeline Syntax: https://www.jenkins.io/doc/book/pipeline/syntax/
2. Flask Microframework Documentation: https://flask.palletsprojects.com/
3. Pro Git Documentation (Scott Chacon & Ben Straub): https://git-scm.com/book/en/v2

---
\pagebreak

# COMPONENT 2: Configuration Management (Ansible) & Kubernetes Deployment (10 Marks)

## 1. Abstract
Component 2 extends the continuous integration pipeline into infrastructure automation and cloud-native container orchestration. Server configuration and service deployment are automated using an Ansible playbook structured with reusable roles, variables, and handlers. The application is containerized using a multi-stage Dockerfile and deployed onto a local Kubernetes cluster with 3 initial replicas and a NodePort service. Dynamic horizontal scaling from 3 to 5 replicas is demonstrated, alongside deployment enhancements including ConfigMaps, liveness/readiness probes, and automated rollback recovery.

## 2. Introduction
Manually provisioning servers and configuring background processes is error-prone and unscalable. Configuration Management tools like Ansible enable Infrastructure as Code (IaC), allowing environments to be reproduced deterministically. Once packaged as a container image via Docker, Kubernetes provides production-grade orchestration: self-healing, rolling updates, health monitoring, and horizontal autoscaling across worker nodes.

## 3. Implementation

### 3.1 Ansible Configuration Management
The Ansible setup consists of an inventory file, a master playbook, and a dedicated role `campus_lab_app`:
- **Inventory (`ansible/inventory.ini`):** Defines target hosts (`[lab_servers] localhost ansible_connection=local`).
- **Variables:** Defined in playbook and defaults (`app_port: 5000`, `app_name: campus-lab-api`, `app_dir: /opt/campus-lab-api`, `artifact_src`).
- **Role (`ansible/roles/campus_lab_app`):**
  - `tasks/main.yml`: Updates package repository, installs runtime dependencies (Python3, pip, tar, curl), unarchives the release package, installs dependencies, templates the systemd unit file, and validates service health.
  - `handlers/main.yml`: Contains `restart campus-lab-api`, which restarts and reloads the service only when files or configs are modified.
  - `templates/campus-lab.service.j2`: Generates `/etc/systemd/system/campus-lab-api.service`.

#### Ansible Execution Command:
```bash
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

### 3.2 Containerization with Docker
A multi-stage `Dockerfile` is utilized to create an optimized production image:
- **Stage 1 (Builder):** Installs compiler and dependencies into an isolated virtual environment (`/opt/venv`).
- **Stage 2 (Runtime):** Copies only the virtual environment and source code onto a lightweight `python:3.12-slim` base, assigns execution to a non-root system user (`appuser`), exposes port 5000, and specifies container health checks.

```bash
docker build -t campus-lab-api:v1 .
docker run -d -p 5000:5000 --name campus-lab-instance campus-lab-api:v1
curl http://localhost:5000/health
```

### 3.3 Kubernetes Deployment & Service Manifests
The application is deployed to Kubernetes with high availability:
- **Deployment (`k8s/deployment.yaml`):** Configures 3 replicas with matching selector `app: campus-lab-api`.
- **Service (`k8s/service.yaml`):** Exposes the deployment externally via a NodePort service on port `30080`.
- **ConfigMap (`k8s/configmap.yaml`):** Externalizes environment variables (`APP_PORT`, `APP_ENV`, `CAMPUS_NAME`).

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 3.4 Scaling Demonstration
Scaling is performed dynamically using `kubectl scale`:
```bash
# Scaling from 3 to 5 pods
kubectl scale deployment campus-lab-deployment --replicas=5
kubectl get pods -l app=campus-lab-api

# Scaling back to 3 pods
kubectl scale deployment campus-lab-deployment --replicas=3
kubectl get pods -l app=campus-lab-api
```

---

## 4. Chosen Deployment Enhancements and Justification

### Selected Enhancements:
1. **Kubernetes ConfigMap for Decoupled Settings:**  
   *Justification:* Hardcoding port numbers or campus department metadata inside deployment manifests violates 12-factor cloud-native app principles. Moving configuration into `k8s/configmap.yaml` allows updating environments without altering the application code or container image.
2. **Liveness and Readiness Probes:**  
   *Justification:* Kubernetes needs to know when a container is ready to receive network traffic (readinessProbe) and when a frozen process needs to be restarted (livenessProbe). Probes configured against `/health` guarantee zero traffic is routed to non-functional pods.
3. **Automated Rollback Demonstration:**  
   *Justification:* Proves disaster recovery capabilities. When a faulty image tag is intentionally deployed, Kubernetes catches the failure, and `kubectl rollout undo` restores the cluster to the preceding operational revision without downtime.

---

## 5. Results & Evidence (Component 2 Screenshots)

### 5.1 Screenshot 1: Ansible Playbook Execution
*Description: Terminal displaying `ansible-playbook -i inventory.ini playbook.yml` output with `changed`, `ok`, and handler trigger notifications.*
```text
[PASTE SCREENSHOT HERE: Ansible playbook run showing PLAY RECAP with successful tasks]
```

### 5.2 Screenshot 2: Docker Image Build & Execution
*Description: Terminal showing `docker build -t campus-lab-api:v1 .` and `docker ps` with running container.*
```text
[PASTE SCREENSHOT HERE: Docker build and docker ps output]
```

### 5.3 Screenshot 3: Kubernetes Pods Before and After Scaling
*Description: Terminal showing `kubectl get pods` displaying 3 running pods, followed by `kubectl scale --replicas=5`, and `kubectl get pods` displaying 5 active pods.*
```text
[PASTE SCREENSHOT HERE: Terminal showing 3 pods, scale command, and 5 pods running]
```

### 5.4 Screenshot 4: Kubernetes Service (`kubectl get svc`)
*Description: Terminal output of `kubectl get svc` displaying `campus-lab-service` NodePort mapping (Port 5000:30080/TCP).*
```text
[PASTE SCREENSHOT HERE: kubectl get svc showing campus-lab-service]
```

### 5.5 Screenshot 5: Application Responding Through Kubernetes Service
*Description: Terminal curl or browser output demonstrating response from `http://localhost:30080/health` or `/api/resources`.*
```text
[PASTE SCREENSHOT HERE: curl output showing JSON response from Kubernetes service]
```

### 5.6 Screenshot 6: Deployment Enhancement (ConfigMap / Probes / Rollback)
*Description: Output of `kubectl describe deployment campus-lab-deployment` displaying Probes and ConfigMap environment references.*
```text
[PASTE SCREENSHOT HERE: kubectl describe deployment showing Liveness, Readiness, and ConfigMap]
```

---

## 6. Conclusion (Component 2)
Component 2 demonstrated automated infrastructure management and cloud-native application orchestration. Ansible automated host provisioning, service installation, and systemd management using reusable roles and handlers. Kubernetes provided elastic horizontal scaling, declarative configuration decoupling via ConfigMaps, health probing, and zero-downtime rollback capabilities.

---

## 7. References (Component 2)
1. Ansible User Guide: https://docs.ansible.com/ansible/latest/user_guide/index.html
2. Kubernetes Documentation (Deployments & Services): https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
3. Docker Best Practices for Python: https://docs.docker.com/language/python/build-images/
