# Security Policy & DevSecOps Controls

CloudOps-Nexus enforces enterprise security principles across the software supply chain, container runtime, and cloud infrastructure.

## Supported Versions

| Version | Supported          | Security Patches |
| ------- | ------------------ | ---------------- |
| 1.0.x   | :white_check_mark: | Active           |
| < 1.0   | :x:                | Deprecated       |

## DevSecOps Controls Implemented

1. **Static Application Security Testing (SAST)**:
   - Automated Bandit scanning on every pull request (`bandit -r app/ -ll`).
   - Linting and AST code security verification via Ruff.

2. **Software Composition Analysis (SCA)**:
   - Automated Dependabot dependency vulnerability alerts and PR generation.
   - Pinned dependencies with verified hashes in `requirements.txt`.

3. **Container Hardening**:
   - Multi-stage minimal builds avoiding build tools in production runtime.
   - Non-root execution (`USER 10001:10001`).
   - Trivy vulnerability scanning blocking high/critical CVEs.

4. **Kubernetes Pod Security Standards**:
   - Namespaces strictly enforce `restricted` pod security standard.
   - `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop all Linux capabilities (`ALL`).
   - Pod Disruption Budgets (`minAvailable: 2`) and zero-trust `NetworkPolicy`.

5. **Infrastructure as Code (IaC) Security**:
   - `tfsec` static analysis checks for AWS security misconfigurations.
   - KMS encryption for EKS secrets at rest.
   - Private subnets for worker nodes with no direct public IPs.

## Reporting a Vulnerability

If you discover a security vulnerability, please do **NOT** open a public issue.

Instead, please send an encrypted email or security advisory to:
- **Security Contact**: psgaikwad2003@gmail.com
- **Response SLA**: Initial acknowledgement within 24 hours; remediation plan within 72 hours.
