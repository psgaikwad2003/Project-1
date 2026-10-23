# CloudOps-Nexus

[![CI/DevSecOps](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue?logo=github-actions)](https://github.com/psgaikwad2003/Project-1/actions)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Multi--Arch-2496ED?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.30-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![Helm](https://img.shields.io/badge/Helm-v3-0F1689?logo=helm)](https://helm.sh/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform%20v1.9-844FBA?logo=terraform)](https://www.terraform.io/)
[![ArgoCD](https://img.shields.io/badge/GitOps-ArgoCD-EF7B4D?logo=argo)](https://argo-cd.readthedocs.io/)
[![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-E6522C?logo=prometheus)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Dashboards-Grafana-F46800?logo=grafana)](https://grafana.com/)
[![Security](https://img.shields.io/badge/DevSecOps-Trivy%20%7C%20Bandit-critical)](https://github.com/aquasecurity/trivy)

**CloudOps-Nexus** is an enterprise-grade, cloud-native microservices platform and automated DevOps ecosystem. Designed according to real-world production engineering practices, this repository incorporates complete **Infrastructure as Code (IaC)**, **Continuous Integration and Continuous Deployment (CI/CD)**, **GitOps**, **Container Hardening**, and **Site Reliability Engineering (SRE) Observability**.

---

## 🏛️ System Architecture

```text
                                  +-----------------------+
                                  |   Developer / PR      |
                                  +-----------+-----------+
                                              |
                                              v
                              +---------------+---------------+
                              |    GitHub Actions CI/CD       |
                              |  - Ruff Lint & Format         |
                              |  - Bandit SAST Security Scan  |
                              |  - Pytest & Code Coverage     |
                              |  - Multi-Arch Docker Build    |
                              |  - Trivy CVE Vulnerability    |
                              +---------------+---------------+
                                              |
                                              v
                              +---------------+---------------+
                              |  GitHub Container Registry    |
                              |    (ghcr.io / Docker Hub)     |
                              +---------------+---------------+
                                              |
                        +---------------------+---------------------+
                        |                                           |
                        v                                           v
       +----------------+----------------+         +----------------+----------------+
       |   Terraform (AWS Cloud IaC)    |         |        ArgoCD GitOps            |
       |  - Multi-AZ VPC Topology        |         |  - Automated Self-Healing Sync  |
       |  - AWS EKS Managed Nodes        |         |  - Helm Chart Package Release   |
       |  - OIDC Provider (IRSA)         |         |  - Multi-Environment Staging/Prd|
       |  - KMS Secrets Encryption       |         +----------------+----------------+
       +----------------+----------------+                          |
                        |                                           |
                        +---------------------+---------------------+
                                              |
                                              v
                    +---------------------------------------------------+
                    |           AWS EKS Kubernetes Cluster              |
                    |                                                   |
                    |   +-------------------+   +-------------------+   |
                    |   |  Ingress (TLS)    |   |  ClusterIP Svc    |   |
                    |   +---------+---------+   +---------+---------+   |
                    |             |                       |             |
                    |             v                       v             |
                    |   +-------------------------------------------+   |
                    |   |  Deployment: Non-Root Pods (3+ Replicas)  |   |
                    |   |  - Probes: /healthz, /readyz, /metrics    |   |
                    |   |  - Zero-Downtime Rolling Updates          |   |
                    |   |  - Horizontal Pod Autoscaler (HPA v2)     |   |
                    |   |  - Pod Disruption Budget (PDB)            |   |
                    |   |  - Zero-Trust NetworkPolicy Segmentation  |   |
                    |   +-------------------------------------------+   |
                    +-------------------------+-------------------------+
                                              |
                                              v
                    +---------------------------------------------------+
                    |         SRE Golden Signals Observability          |
                    |  - Prometheus Scraper & Alert Rules (5xx, P99)    |
                    |  - Grafana Dashboards: Latency, Throughput, Sat.  |
                    |  - Structured JSON Logging with Correlation IDs   |
                    +---------------------------------------------------+
```

---

## 📁 Repository Layout

```text
Project-1/
├── .github/
│   ├── dependabot.yml              # Automated dependency update configuration
│   └── workflows/
│       ├── ci.yml                  # Linting, SAST, Pytest, Multi-Arch Docker Build & Trivy Scan
│       ├── cd.yml                  # Automated CD pipeline with Staging & Production gates
│       └── terraform-ci.yml        # Terraform fmt, validate, and tfsec security scan
├── app/
│   ├── .env.example                # 12-factor environment variables specification
│   ├── config.py                   # Pydantic Settings application configuration
│   ├── logger.py                   # Structured JSON logging with Correlation ID injection
│   ├── metrics.py                  # Prometheus Golden Signals metrics instrumentation
│   ├── requirements.txt            # Production dependencies with pinned versions
│   └── main.py                     # High-performance FastAPI REST API with health probes
├── tests/
│   ├── __init__.py                 # Test package initialization
│   └── test_main.py                # End-to-end endpoint, health check, and metrics test suite
├── Dockerfile                      # Production multi-stage minimal non-root Dockerfile
├── .dockerignore                   # Build context exclusions for rapid builds and security
├── docker-compose.yml              # Full-stack local production-parity environment
├── docker-compose.override.yml     # Local hot-reloading development overrides
├── terraform/
│   ├── versions.tf                 # Terraform provider constraints & remote S3 backend
│   ├── variables.tf                # Typed input variables with validation rules
│   ├── terraform.tfvars.example    # Example environment variable assignments
│   ├── main.tf                     # Root infrastructure composition module
│   ├── outputs.tf                  # Cluster endpoints, VPC IDs, and kubeconfig helper
│   └── modules/
│       ├── vpc/                    # Multi-AZ VPC, subnets, NAT Gateway, route tables
│       └── eks/                    # AWS EKS cluster, managed node groups, KMS, IRSA
├── k8s/
│   ├── namespace.yaml              # Namespace with Pod Security Standards & Quotas
│   ├── configmap.yaml              # Decoupled application configuration
│   ├── secret.yaml                 # Sensitive credentials template
│   ├── deployment.yaml             # Resilient Deployment with probes, HPA & security context
│   ├── service.yaml                # ClusterIP service definition
│   ├── ingress.yaml                # Nginx Ingress with SSL/TLS termination
│   ├── hpa.yaml                    # Horizontal Pod Autoscaler v2 (CPU & Memory metrics)
│   ├── pdb.yaml                    # PodDisruptionBudget ensuring 99.99% availability
│   └── network-policy.yaml         # Zero-trust network segmentation
├── helm/
│   └── cloudops-nexus/
│       ├── Chart.yaml              # Helm Chart v2 definition
│       ├── values.yaml             # Extensively documented chart values
│       └── templates/              # Production Helm templates (_helpers, deployment, svc, etc.)
├── argocd/
│   ├── project.yaml                # ArgoCD AppProject RBAC and repository restrictions
│   └── application.yaml            # ArgoCD Application CRD with automated sync and self-heal
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml          # Prometheus scrape configuration with k8s pod discovery
│   │   └── alert-rules.yaml        # SRE Alerting rules for 5xx errors and P99 latency
│   └── grafana/
│       └── dashboards/
│           └── application-performance.json  # Comprehensive Grafana dashboard
├── Makefile                        # Enterprise automation CLI for developers and CI runners
├── .pre-commit-config.yaml         # Git hooks for code quality, formatting, and secret scanning
├── .editorconfig                   # Unified cross-editor indentation and newline standard
├── .gitignore                      # Exhaustive gitignore for Python, Terraform, Docker, and K8s
├── SECURITY.md                     # Security policies and vulnerability reporting procedures
├── CONTRIBUTING.md                 # Contribution workflow, branching strategy, and guidelines
└── README.md                       # Platform documentation and architecture overview
```

---

## 🚀 Quickstart: Local Development

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Make (optional, for developer shortcuts)

### 2. Start Full Stack with Docker Compose
Run the entire production-parity ecosystem (API, PostgreSQL, Redis, Prometheus, Grafana) with a single command:
```bash
make compose-up
# Or directly: docker-compose up -d --build
```

### 3. Verify Local Services
| Service | URL | Default Credentials |
| ------- | --- | ------------------- |
| **CloudOps API** | [http://localhost:8000](http://localhost:8000) | N/A |
| **Interactive Docs (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) | N/A |
| **Health Check (Liveness)** | [http://localhost:8000/healthz](http://localhost:8000/healthz) | N/A |
| **Readiness Check** | [http://localhost:8000/readyz](http://localhost:8000/readyz) | N/A |
| **Prometheus Metrics** | [http://localhost:8000/metrics](http://localhost:8000/metrics) | N/A |
| **Prometheus Server** | [http://localhost:9090](http://localhost:9090) | N/A |
| **Grafana Dashboards** | [http://localhost:3000](http://localhost:3000) | `admin` / `admin` |

### 4. Running Tests & Quality Checks
```bash
# Run unit & integration test suite with coverage
make test

# Run code linter
make lint

# Run security SAST scan
make security-scan
```

---

## ☁️ Infrastructure as Code (AWS EKS via Terraform)

The infrastructure is completely modularized under `terraform/`.

### 1. Initialize and Validate
```bash
cd terraform
terraform init
terraform validate
```

### 2. Plan and Deploy
```bash
# Preview infrastructure changes
terraform plan

# Apply infrastructure to AWS
terraform apply -auto-approve
```

### 3. Connect kubectl to EKS
```bash
aws eks --region us-east-1 update-kubeconfig --name cloudops-nexus-prod
kubectl get nodes
```

---

## ☸️ Kubernetes & Helm Deployment

### Deploy via Raw Manifests
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

### Deploy via Helm Chart
```bash
# Lint the chart
helm lint helm/cloudops-nexus

# Deploy to cluster
helm upgrade --install cloudops-nexus helm/cloudops-nexus \
  --namespace cloudops \
  --create-namespace \
  --values helm/cloudops-nexus/values.yaml
```

---

## 🔄 GitOps with ArgoCD

ArgoCD automatically detects changes pushed to the repository and synchronizes the cluster state:

1. **Apply the ArgoCD AppProject**:
   ```bash
   kubectl apply -f argocd/project.yaml
   ```

2. **Deploy the ArgoCD Application**:
   ```bash
   kubectl apply -f argocd/application.yaml
   ```

3. **Verify GitOps Sync Status**:
   ```bash
   argocd app get cloudops-nexus
   ```

---

## 🛡️ DevSecOps & Security Posture

- **Least Privilege**: Pods run as unprivileged user `10001:10001` with `readOnlyRootFilesystem` and dropped capabilities.
- **Vulnerability Scanning**: Automated Trivy scans block container images containing High or Critical CVEs.
- **Static Analysis**: Bandit scans Python code for injection risks and insecure configurations.
- **Secrets Management**: KMS-encrypted secrets at rest in AWS EKS and external secret injection support.
- **Zero-Trust Network Policies**: Pod traffic isolated with explicit ingress and egress permissions.

---

## 📈 Observability & SRE Alerting

- **Golden Signals**: Instrumenting Latency (p50/p90/p99), Traffic (RPS), Errors (5xx rate), and Saturation (CPU/Memory).
- **Proactive Alerts**:
  - `HighHttpErrorRate5xx`: Triggers when HTTP 5xx responses exceed 5% over a 5-minute window.
  - `HighRequestLatencyP99`: Fires when 99th percentile response time breaches 1.5 seconds.
  - `HighMemorySaturation`: Triggers when container memory consumption exceeds 85%.

---

## 🤝 Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, branch conventions, and development procedures.

## 📄 License

This project is open-source and licensed under the [Apache 2.0 License](LICENSE).
