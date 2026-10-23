# Contributing to CloudOps-Nexus

Thank you for contributing to the CloudOps-Nexus platform! This guide outlines our standard operating procedures for code and infrastructure contributions.

## Branching Strategy

We follow the **Trunk-Based Development** pattern with short-lived feature branches:

- `main`: Production-ready branch. Direct pushes to `main` are protected; changes require PR approval.
- `feat/<feature-name>`: New feature implementations.
- `fix/<bug-name>`: Bug fixes and patches.
- `infra/<resource-name>`: Infrastructure and Terraform modifications.
- `ci/<pipeline-name>`: CI/CD workflow updates.

## Commit Message Convention

We strictly follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

### Supported Types:
- `feat`: A new feature or capability
- `fix`: A bug fix
- `infra`: Terraform, AWS, or cloud resource changes
- `k8s`: Kubernetes manifests and Helm charts
- `ci`: CI/CD workflows and automation scripts
- `observability`: Prometheus, Grafana, or logging changes
- `docs`: Documentation updates
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks or dependency bumps

## Local Development Workflow

1. **Clone the repository**:
   ```bash
   git clone https://github.com/psgaikwad2003/Project-1.git
   cd Project-1
   ```

2. **Setup virtual environment & hooks**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   make setup
   ```

3. **Run tests**:
   ```bash
   make test
   ```

4. **Run linters**:
   ```bash
   make lint
   ```

5. **Start local multi-container stack**:
   ```bash
   make compose-up
   ```

## Pull Request Checklist

Before submitting a PR, ensure:
- [ ] Code passes all unit tests (`make test`).
- [ ] Linters pass without errors (`make lint`).
- [ ] No security vulnerabilities flagged by Bandit (`make security-scan`).
- [ ] Commit history is clean with clear conventional commit messages.
- [ ] Relevant documentation has been updated.
