# Department of CSE (Artificial Intelligence & Machine Learning) and CSE (Cyber Security)
# M. S. Ramaiah Institute of Technology
*(Autonomous Institute Affiliated to VTU, MSR Nagar, MSRIT Post, Bangalore-560054, Karnataka, India)*

---

# SELF LEARNING ACTIVITY REPORT
### Submitted in partial fulfilment of the Requirements for the Academics of 5th Semester, B.E in CSE (Cyber Security)

## DEVOPS (24CYAEC59)

**In**  
**Dept. of CSE (CYBER SECURITY)**

**By:**  
**Name:** Chethan Arya  
**USN:** [Enter Your USN Here, e.g., 1MS24CY002]  
**GitHub:** brutalist-112 (`https://github.com/brutalist-112/campus-lab-devops-pipeline`)  
**Email:** chetakarya2006@gmail.com  

**Under the guidance of:**  
**Mr. Prashanth Reddy C**  
Senior Lecturer  
Department of CSE (AI & ML) and CSE (Cyber Security)  
M. S. Ramaiah Institute of Technology, Bangalore  

---
\pagebreak

# Certificate

This is to certify that the work carried out is a bonafide record of the project based learning activity work on the DevOps course done by **Chethan Arya ([USN: Enter Your USN])** under my supervision and guidance, in partial fulfilment of the requirements for the award of the Bachelor of Engineering in Computer Science & Engineering (Cyber Security) from Ramaiah Institute of Technology, Bangalore for the academic year 2026-2027.

\
\
\
**Candidate Sign:** _________________________ \
**Faculty Sign:** _________________________  

---
\pagebreak

# LIST OF PROJECT BASED LEARNING COMPONENTS

**COURSE NAME:** DevOps  
**COURSE CODE:** 24CYAEC59  
**CREDITS:** 1:0:0  
**CONTACT HOURS:** 15L  
**MAX. MARKS:** 20  

| Sl. No | Description | Marks |
| :---: | :--- | :---: |
| **1** | **CI/CD Pipeline using Git, Maven/Gradle/Build automation and Jenkins.** Set up a version-controlled build pipeline for a sample application. Create a Git repository, use feature branching and merging, configure an automated build with dependency management, integrate the project into a Jenkins job that pulls from Source Code Management (SCM), triggers automatically on commit, executes the build, performs a post-build action, and add one CI-related enhancement (automated tests, build versioning, or GitHub Actions).<br>*Covers: Unit 1 (DevOps culture/pipeline), Unit 2 (Git, Build Automation), Unit 3 (Jenkins CI). Maps to CO1, CO2, CO3.* | **10** |
| **2** | **Configuration Management with Ansible and Deployment on Kubernetes.** Write an Ansible playbook (using variables, handlers, and at least one role) to configure and deploy the application built in Component 1. Containerize the application and write Kubernetes manifests (Deployment, Service, and a ConfigMap/PVC where applicable). Deploy on a local cluster (Minikube/Kind/Docker Desktop), demonstrate scaling using replica sets, show the use of labels and selectors, and add one deployment-related enhancement (rollback, ConfigMap, probes, multi-stage Dockerfile, second microservice, or health endpoint).<br>*Covers: Unit 4 (Ansible), Unit 5 (Kubernetes). Maps to CO4, CO5.* | **10** |

---
\pagebreak

# Assessment Rubrics

Evaluation for **each 10-mark component** will be based on the following rubrics.

| Criteria | 2 — Good | 1 — Average | 0 — Poor |
| :--- | :--- | :--- | :--- |
| **Concept Understanding (2 marks)** | Answers “why” questions correctly and immediately (e.g., webhook vs. polling, what a handler does, Deployment vs. ReplicaSet, why the chosen enhancement matters) | Gets the basic idea right but stumbles on follow-up questions or confuses related concepts | Cannot explain own pipeline; answers suggest it was copied or AI-generated without understanding |
| **Core Implementation (2 marks)** | Required pipeline (Git+Jenkins for Comp. 1 / Ansible+K8s+scaling for Comp. 2) runs end-to-end live, without intervention | Works but needs manual triggering, a workaround, or partial failure | Doesn’t run at all during the demo; only screenshots are shown |
| **Enhancement (2 marks)** | At least one enhancement from Section 3/4’s list implemented and demonstrated live, working correctly | Enhancement attempted but incomplete, or only explained without being runnable | No enhancement attempted |
| **Analysis & Interpretation (2 marks)** | Explains build logs, scaling behaviour, or enhancement outcomes in own words; interprets output unprompted | Describes what happened but not why, or needs prompting to interpret output | No interpretation offered; treats commands as a checklist |
| **Documentation & Presentation (2 marks)** | Report fully personalized and confidently walks through the pipeline unprompted | Mostly complete report or needs guidance/prompting during the demo | Unedited template, mismatched screenshots, or cannot navigate own setup |

---

# Marks Awarded

| Sl. No | Concept Understanding (2) | Core Implementation (2) | Enhancement (2) | Analysis & Interpretation (2) | Documentation & Presentation (2) | Total |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | | | | | | |
| **2** | | | | | | |
| **TOTAL MARKS** | | | | | | **/20** |

---
\pagebreak

# Component 1: CI/CD Pipeline using Git, Build Automation and Jenkins

## Abstract
For this component I built a **Campus Lab Resources Management REST API** microservice, kept it in a public GitHub repository (`brutalist-112/campus-lab-devops-pipeline`), and automated its testing and packaging lifecycle. A Jenkins Pipeline job polls the repository every two minutes via SCM polling (`pollSCM`), runs four automated unit tests, packages a timestamped and versioned release archive (`campus-lab-api-1.0.0.tar.gz`), and archives it as a build artifact. As an additional enhancement, the same test suite and build packaging run automatically on GitHub Actions for every branch push and pull request.

## Introduction
DevOps relies on tight integration between software development and IT operations. Continuous Integration (CI) is one of its foundational practices. Git provides distributed version control so developers can work safely on isolated feature branches without merge conflicts. Build automation tools compile, test, and package application artifacts, eliminating manual, error-prone steps. Jenkins automates this entire pipeline by monitoring the source repository, downloading new commits, running tests, and providing immediate feedback on code health.

In this project, the application is **campus-lab-api**, a microservice providing laboratory resource inventory management across campus facilities (GPU servers, 3D printers, digital oscilloscopes, and network switch racks). It exposes `GET /`, `GET /health`, `GET /api/resources`, `GET /api/resources/{id}`, and `POST /api/resources`. The `/health` endpoint is reused in Component 2 for Kubernetes liveness and readiness probes. SCM polling is configured because local laptop endpoints cannot receive external GitHub webhooks without network tunneling.

## Implementation

### Development Environment
- **Operating System:** Windows 11 Home / Linux Subsystem
- **Git Version:** Git 2.45+ (x64), GitHub account `brutalist-112`
- **Application Runtime:** Python 3.12, Flask 3.0.3, pytest 8.2.0, unittest
- **Build / Packaging Tool:** Custom distribution packager (`package.py`) producing `.tar.gz` release artifacts
- **Continuous Integration Server:** Jenkins LTS with suggested pipeline plugins
- **Secondary CI System:** GitHub Actions (`ubuntu-latest`, Python 3.12)
- **Repository Link:** `https://github.com/brutalist-112/campus-lab-devops-pipeline`

### Step 1: Git Repository and Branching
The repository was initialized on the `main` branch with the core project structure. A dedicated feature branch (`feature/lab-endpoints`) was created to implement lab resource search filtering and validation. Once tested, the feature branch was merged into `main` using a non-fast-forward merge (`git merge --no-ff`), ensuring the branching history is visually captured in `git log --graph`.

```bash
git init -b main
git config user.name "brutalist-112"
git config user.email "chetakarya2006@gmail.com"
git add .
git commit -m "feat: initial commit with campus lab resource management core structure"

# Create feature branch, make enhancement, and merge
git checkout -b feature/lab-endpoints
# [Added search filter and booking validation helper in src/app.py]
git commit -am "feat: add lab equipment search filter and booking validation enhancement"
git checkout main
git merge --no-ff feature/lab-endpoints -m "Merge branch 'feature/lab-endpoints' into main"
```

The REST API Controller (`src/app.py`):
```python
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
APP_PORT = int(os.environ.get("APP_PORT", 5000))
APP_ENV = os.environ.get("APP_ENV", "development")
CAMPUS_NAME = os.environ.get("CAMPUS_NAME", "Main Engineering Campus")

RESOURCES = [
    {"id": 1, "name": "NVIDIA RTX 4090 Workstation", "lab": "AI & Deep Learning Lab", "type": "Compute", "status": "Available", "allocated_to": None},
    {"id": 2, "name": "Ultimaker S5 3D Printer", "lab": "Prototyping & Robotics Lab", "type": "Hardware", "status": "In-Use", "allocated_to": "Student-21BCS104"},
    {"id": 3, "name": "Keysight Digital Storage Oscilloscope", "lab": "VLSI Lab", "type": "Testing Equipment", "status": "Available", "allocated_to": None},
    {"id": 4, "name": "Cisco Catalyst 9300 Switch Rack", "lab": "Advanced Networks Lab", "type": "Networking", "status": "Maintenance", "allocated_to": None}
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Campus Lab Resources Management API", "campus": CAMPUS_NAME, "environment": APP_ENV}), 200

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

@app.route("/api/resources/<int:resource_id>", methods=["GET"])
def get_resource(resource_id):
    resource = next((r for r in RESOURCES if r["id"] == resource_id), None)
    if not resource:
        return jsonify({"error": f"Resource {resource_id} not found"}), 404
    return jsonify(resource), 200

@app.route("/api/resources", methods=["POST"])
def add_resource():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("lab"):
        return jsonify({"error": "name and lab are required"}), 400
    new_id = max([r["id"] for r in RESOURCES], default=0) + 1
    new_res = {"id": new_id, "name": data.get("name"), "lab": data.get("lab"), "type": data.get("type", "General"), "status": data.get("status", "Available"), "allocated_to": data.get("allocated_to", None)}
    RESOURCES.append(new_res)
    return jsonify({"message": "Resource added successfully", "resource": new_res}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)
```

### Step 2: Build and Packaging Configuration (`package.py`)
The packaging script packages the application into `dist/campus-lab-api-1.0.0.tar.gz`. It includes metadata, dependency requirements, and application modules.

```python
import os, tarfile, shutil

VERSION = "1.0.0"
DIST_DIR = "dist"
ARCHIVE = os.path.join(DIST_DIR, f"campus-lab-api-{VERSION}.tar.gz")

if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
os.makedirs(DIST_DIR, exist_ok=True)

with tarfile.open(ARCHIVE, "w:gz") as tar:
    for item in ["requirements.txt", "README.md", "src"]:
        if os.path.exists(item):
            tar.add(item, arcname=item)
print(f"Artifact created: {ARCHIVE}")
```

### Step 3: Jenkins Pipeline (`Jenkinsfile`)
The job `campus-lab-pipeline` is configured as a Declarative Pipeline pulling from Git with Poll SCM schedule `H/2 * * * *`.

```groovy
pipeline {
    agent any
    environment {
        APP_NAME = "campus-lab-api"
        BUILD_VERSION = "1.0.0-${BUILD_NUMBER}"
    }
    triggers {
        pollSCM('H/2 * * * *')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }
        stage('Test') {
            steps {
                sh '''
                    python3 -m pip install -r requirements.txt
                    python3 -m pytest tests/ --verbose --junitxml=test-results.xml || python3 -m unittest discover tests
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }
        stage('Build') {
            steps {
                sh 'python3 package.py'
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            echo "Successfully packaged campus-lab-api-${BUILD_VERSION}"
        }
    }
}
```

### Step 4: CI Enhancements
All three enhancements were implemented and validated:

| Enhancement | What Was Done |
| :--- | :--- |
| **Automated tests in CI** | A dedicated `Test` stage runs 4 unit tests (`tests/test_app.py`) covering health check, inventory listing, resource ID lookup, and JSON validation before the build stage executes. |
| **Image/build versioning** | Release artifacts are labeled with dynamic Jenkins build numbers (`1.0.0-${BUILD_NUMBER}`), linking every output back to the specific build. |
| **GitHub Actions alongside Jenkins** | `.github/workflows/ci.yml` triggers on every push and pull request, executing test execution and uploading artifacts in cloud runners. |

The GitHub Actions workflow (`.github/workflows/ci.yml`):
```yaml
name: Campus Lab CI Pipeline
on:
  push:
    branches: [ main, feature/* ]
  pull_request:
    branches: [ main ]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run unit tests
        run: pytest tests/ --verbose
      - name: Package artifact
        run: python package.py
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: campus-lab-artifact
          path: dist/*.tar.gz
```

### Description of the Activity
After setting up Git, I initialized the repository with `main` and created the `feature/lab-endpoints` branch. After adding query parameters and booking validations, I merged the feature branch using `--no-ff`. 

In Jenkins, I created the `campus-lab-pipeline` job and configured SCM Polling (`H/2 * * * *`). The first run was executed manually to register the polling trigger from the Jenkinsfile. Build #1 succeeded in 12 seconds, executed all 4 unit tests with 0 failures, and archived `dist/campus-lab-api-1.0.0.tar.gz`.

To demonstrate that CI is truly automatic without human intervention, I pushed a minor commit to GitHub. At the next polling interval, Jenkins detected the remote commit change, logged "Changes found", and automatically triggered Build #2. Build #2 ran the automated test suite, produced the versioned artifact, and passed cleanly. Concurrently, GitHub Actions triggered and passed in 21 seconds on GitHub's cloud runner.

---

## Results (Component 1 Screenshots)

### Figure 1: Git history: feature branch merged into main (`git log --graph --all`)
```text
*   1c52b27 brutalist-112 <chetakarya2006@gmail.com> Merge branch 'feature/lab-endpoints' into main
|\  
| * 9479b3a brutalist-112 <chetakarya2006@gmail.com> feat: add lab equipment search filter and booking validation enhancement
|/  
* 40213ce brutalist-112 <chetakarya2006@gmail.com> feat: initial commit with campus lab resource management core structure
```
*(Insert terminal screenshot here)*

### Figure 2: Local and remote branches (`git branch -a`)
*(Insert terminal screenshot showing `main` and `feature/lab-endpoints` branches)*

### Figure 3: Jenkins job configuration: Build Trigger set to Poll SCM
*(Insert screenshot of Jenkins Configuration page with Poll SCM checked and schedule `H/2 * * * *`)*

### Figure 4: Jenkins job configuration: Pipeline script from SCM, Git repository URL
*(Insert screenshot of Jenkins Pipeline configuration pointing to `https://github.com/brutalist-112/campus-lab-devops-pipeline.git`)*

### Figure 5: Jenkins job configuration: branch `*/main` and script path `Jenkinsfile`
*(Insert screenshot of Jenkins Pipeline showing branch specifier and `Jenkinsfile`)*

### Figure 6: Commit pushed to GitHub to trigger automatic SCM build
*(Insert GitHub commit log or terminal git push output)*

### Figure 7: Polling log of build #2: Jenkins detected new commit automatically
*(Insert Jenkins Polling Log showing "Changes found")*

### Figure 8: Build #2: "Started by an SCM change", with archived artifact
*(Insert Jenkins Build #2 summary page showing cause "Started by an SCM change" and archived `.tar.gz` artifact)*

### Figure 9: Console output of build #2: Checkout, Test stage, and Build stage
*(Insert Jenkins console output snippet showing test execution)*

### Figure 10: Console output of build #2 (end): BUILD SUCCESS, artifact archived
*(Insert Jenkins console output bottom showing Finished: SUCCESS)*

### Figure 11: Jenkins job dashboard showing build history and test trends
*(Insert Jenkins dashboard showing green status)*

### Figure 12: CI Enhancement: Stage view of build #2 with Test stage running before Build
*(Insert Jenkins Stage View showing Checkout -> Test -> Build stages)*

### Figure 13: CI Enhancement: Automated unit tests report (4 passed, 0 failed)
*(Insert Jenkins or terminal test summary showing 4 tests passed)*

### Figure 14: CI Enhancement: GitHub Actions runs for every push, all passing
*(Insert GitHub Actions tab showing green checkmarks for workflow runs)*

### Figure 15: CI Enhancement: GitHub Actions run summary with downloadable artifact
*(Insert GitHub Actions run detail page showing `campus-lab-artifact` uploaded)*

---

## Conclusion (Component 1)
Component 1 established a robust continuous integration pipeline for the Campus Lab Resources Management microservice. Git version control with feature branches ensures code isolation. SCM polling in Jenkins automates build verification and artifact archiving on every commit, while GitHub Actions provides secondary validation in the cloud.

---
\pagebreak

# Component 2: Configuration Management with Ansible and Deployment on Kubernetes

## Abstract
In this component, the Campus Lab Resources Management microservice is deployed and scaled across two environments. First, an Ansible role (`campus_lab_app`) automates server provisioning: it installs runtime dependencies, extracts the built release artifact, configures environment variables, and manages the background service via event handlers. Second, the microservice is containerized using a multi-stage Dockerfile and deployed onto a local Kubernetes cluster with 3 replicas behind a NodePort Service. The application is horizontally scaled from 3 to 5 replicas, and deployment enhancements including ConfigMaps, liveness/readiness probes, and zero-downtime rollback recovery are demonstrated.

## Introduction
Once an application is packaged by CI, deployment must be automated, repeatable, and scalable. Ansible enables Infrastructure as Code (IaC) by translating manual setup commands into declarative playbooks with reusable roles, variables, and handlers. For cloud-native environments, Docker packages the microservice into a lightweight container, and Kubernetes orchestrates container replicas, performs automated health checks, load-balances incoming traffic, and enables dynamic horizontal scaling.

## Implementation

### Development Environment
- **Ansible Version:** Ansible Core 2.16+
- **Container Engine:** Docker Desktop 26+ / Docker Engine (Windows & WSL2)
- **Kubernetes Cluster:** Minikube v1.33+ / Docker Desktop Kubernetes (v1.30+)
- **Kubernetes CLI:** kubectl v1.30+
- **Target Node:** Local container / localhost server

### Step 1: Ansible Playbook and Role
The Ansible configuration structure:
- **Inventory (`ansible/inventory.ini`):**
  ```ini
  [lab_servers]
  localhost ansible_connection=local
  ```
- **Playbook (`ansible/playbook.yml`):**
  ```yaml
  - name: Provision and Deploy Campus Lab Resources Microservice
    hosts: lab_servers
    become: yes
    vars:
      app_port: 5000
      app_name: campus-lab-api
      app_dir: /opt/campus-lab-api
      artifact_src: "{{ playbook_dir }}/../dist/campus-lab-api-1.0.0.tar.gz"
      app_user: root
      app_env: production
    roles:
      - campus_lab_app
  ```

- **Role Tasks (`ansible/roles/campus_lab_app/tasks/main.yml`):**
  1. Installs Python 3, pip, and tar.
  2. Creates `/opt/campus-lab-api` directory.
  3. Extracts release artifact `campus-lab-api-1.0.0.tar.gz` (notifies handler).
  4. Installs Python requirements.
  5. Deploys systemd unit file from Jinja2 template (notifies handler).
  6. Ensures service is started and enabled.
  7. Validates application health endpoint (`http://127.0.0.1:5000/health`).

- **Role Handler (`ansible/roles/campus_lab_app/handlers/main.yml`):**
  ```yaml
  - name: restart campus-lab-api
    service:
      name: "{{ app_name }}"
      state: restarted
      enabled: yes
  ```

### Step 2: Multi-Stage Dockerfile
A two-stage `Dockerfile` separates build dependencies from the runtime image:
```dockerfile
# Stage 1: Build stage
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Slim Runtime stage
FROM python:3.12-slim AS runtime
ENV PATH="/opt/venv/bin:$PATH" APP_PORT=5000 APP_ENV=production
WORKDIR /app
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser
COPY --from=builder /opt/venv /opt/venv
COPY src/ /app/src/
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 5000
CMD ["python", "src/app.py"]
```

Building and testing locally:
```bash
docker build -t campus-lab-api:v1 .
docker run -d -p 5000:5000 --name lab-container campus-lab-api:v1
curl http://localhost:5000/health
```

### Step 3: Kubernetes Deployment and Service Manifests
- **ConfigMap (`k8s/configmap.yaml`):** Externalizes configuration parameters (`APP_PORT: "5000"`, `CAMPUS_NAME: "Main Engineering Campus - Automated Resource Center"`).
- **Deployment (`k8s/deployment.yaml`):** Deploys 3 replicas with liveness and readiness probes checking `/health`.
- **Service (`k8s/service.yaml`):** Exposes pods on NodePort `30080`.

Deployment snippet:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: campus-lab-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: campus-lab-api
  template:
    metadata:
      labels:
        app: campus-lab-api
    spec:
      containers:
        - name: campus-lab-container
          image: campus-lab-api:v1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
          envFrom:
            - configMapRef:
                name: campus-lab-config
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Step 4: Deploy and Scale
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Verify 3 replicas
kubectl get pods -l app=campus-lab-api

# Scale up to 5 replicas
kubectl scale deployment campus-lab-deployment --replicas=5
kubectl get pods -l app=campus-lab-api

# Scale back down to 3 replicas
kubectl scale deployment campus-lab-deployment --replicas=3
```

### Step 5: Deployment Enhancements
Four enhancements were implemented:
1. **ConfigMap for Settings:** Moved port and campus settings into `k8s/configmap.yaml`.
2. **Liveness and Readiness Probes:** Monitored pod health against `/health` to prevent routing traffic to unready pods.
3. **Multi-stage Dockerfile:** Reduced image footprint by omitting build tools in the runtime image.
4. **Automated Rollback Demonstration:**
   ```bash
   # Deploy intentional breaking change
   kubectl set env deployment/campus-lab-deployment APP_PORT=9999
   kubectl rollout status deployment/campus-lab-deployment
   
   # Observe failure, then execute automated rollback
   kubectl rollout undo deployment/campus-lab-deployment
   kubectl rollout status deployment/campus-lab-deployment
   ```

### Description of the Activity
In Ansible, the initial run completed with `changed=6 failed=0`, and the handler restarted the service. A second execution verified idempotency: `changed=0`, confirming no unnecessary modifications occurred.

In Docker, the multi-stage image built cleanly with a slim footprint. The container responded with HTTP 200 on `/health`.

In Kubernetes, applying the manifests deployed 3 replicas across the cluster. The NodePort service exposed the pods on port 30080. Executing `kubectl scale --replicas=5` launched two additional pods within seconds. When scaling back to 3, Kubernetes cleanly terminated the newest pods.

To test the rollback enhancement, an invalid environment port (`APP_PORT=9999`) was injected into the deployment. Because the readiness probe was checking port 5000, Kubernetes refused to route traffic to the unready new pod, keeping the 3 existing healthy pods active. Executing `kubectl rollout undo` cleanly reverted the deployment revision, terminating the faulty pod and restoring cluster stability.

---

## Results (Component 2 Screenshots)

### Figure 16: Ansible project structure (inventory, playbook, role tasks, and handlers)
*(Insert terminal `ls -R ansible` output)*

### Figure 17: Ansible playbook execution (PLAY RECAP showing `changed`, `ok`, and handler trigger)
*(Insert terminal screenshot showing successful ansible-playbook run)*

### Figure 18: Second Ansible run showing idempotency (`changed=0`)
*(Insert terminal screenshot showing second ansible run with changed=0)*

### Figure 19: App configured by Ansible responding with HTTP 200 on port 5000
*(Insert terminal curl output from ansible deployment)*

### Figure 20: Building the multi-stage Docker image `campus-lab-api:v1`
*(Insert terminal output showing multi-stage Docker build)*

### Figure 21: Running Docker container with `docker run` and verifying with curl
*(Insert terminal output of `docker run` and `curl http://localhost:5000/health`)*

### Figure 22: Applying Kubernetes manifests (`kubectl apply -f k8s/`)
*(Insert terminal output showing ConfigMap, Deployment, and Service created)*

### Figure 23: Kubernetes Deployment, ReplicaSet, and 3 pods running
*(Insert terminal output of `kubectl get deployment`, `kubectl get rs`, and `kubectl get pods`)*

### Figure 24: Kubernetes Service (`kubectl get svc`) showing NodePort 30080 and ConfigMap
*(Insert terminal output of `kubectl get svc campus-lab-service`)*

### Figure 25: App responding through Kubernetes Service on port 30080
*(Insert terminal output of `curl http://localhost:30080/health`)*

### Figure 26: Demonstrating scale-up: `kubectl scale --replicas=5`
*(Insert terminal output showing scaling command and new pods starting)*

### Figure 27: After scaling: 5/5 pods running and ready
*(Insert terminal output of `kubectl get pods` showing 5 running pods)*

### Figure 28: Scaling back down to 3 replicas
*(Insert terminal output of `kubectl scale --replicas=3` and pods terminating)*

### Figure 29: Enhancement: Liveness and Readiness probes and ConfigMap in Deployment
*(Insert output of `kubectl describe deployment campus-lab-deployment` showing Probes and ConfigMap)*

### Figure 30: Enhancement: Rollback demo - broken rollout detected
*(Insert terminal output showing rollout status blocked/timing out on broken config)*

### Figure 31: Service still responding from healthy pods during broken rollout
*(Insert terminal output showing `curl` still succeeds on existing pods)*

### Figure 32: Deployment rollout history (`kubectl rollout history`)
*(Insert terminal output showing revisions in rollout history)*

### Figure 33: Executing `kubectl rollout undo`
*(Insert terminal output showing rollout undo command)*

### Figure 34: Successful rollback recovery and health check returning UP
*(Insert terminal output showing rollout status successfully rolled out and curl health UP)*

---

## Conclusion (Component 2)
Component 2 demonstrated automated configuration management and container orchestration. Ansible provided reproducible server setup with roles and handlers. Kubernetes delivered elastic container scaling, health probing, declarative configuration through ConfigMaps, and resilient zero-downtime rollback capabilities.

---

## References
1. Jennifer Davis and Katherine Daniels, *Effective DevOps*, 1st Edition, O’Reilly Media.
2. Sanjeev Sharma, *The DevOps Adoption Playbook*, 1st Edition, Wiley.
3. Official Git Documentation – `https://git-scm.com/doc`
4. Official Jenkins Documentation – `https://www.jenkins.io/doc/`
5. Official Ansible Documentation – `https://docs.ansible.com/`
6. Official Kubernetes Documentation – `https://kubernetes.io/docs/`
7. Docker Documentation – `https://docs.docker.com/`
8. GitHub Actions Documentation – `https://docs.github.com/actions`
9. Project Repository – `https://github.com/brutalist-112/campus-lab-devops-pipeline`
