SHELL := /bin/bash
.DEFAULT_GOAL := help

APP_NAME := cloudops-nexus
IMAGE_NAME := psgaikwad2003/$(APP_NAME)
VERSION ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "v1.0.0")

.PHONY: help
help: ## Display available commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: setup
setup: ## Install local dependencies and pre-commit hooks
	pip install -r app/requirements.txt
	pre-commit install

.PHONY: lint
lint: ## Run code linters (ruff, black)
	ruff check .
	ruff format --check .

.PHONY: lint-fix
lint-fix: ## Automatically fix linting and formatting issues
	ruff check --fix .
	ruff format .

.PHONY: test
test: ## Run unit tests with code coverage
	pytest --cov=app --cov-report=term-missing --cov-report=xml tests/

.PHONY: security-scan
security-scan: ## Run vulnerability and SAST scans
	bandit -r app/ -ll
	trivy fs --severity HIGH,CRITICAL .

.PHONY: docker-build
docker-build: ## Build Docker container image
	docker build -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .

.PHONY: docker-run
docker-run: ## Run Docker container locally
	docker run -p 8000:8000 --env-file app/.env.example $(IMAGE_NAME):latest

.PHONY: compose-up
compose-up: ## Start full local stack with docker-compose
	docker-compose up -d --build

.PHONY: compose-down
compose-down: ## Stop local docker-compose environment
	docker-compose down -v

.PHONY: tf-init
tf-init: ## Initialize Terraform providers and backend
	cd terraform && terraform init

.PHONY: tf-plan
tf-plan: ## Run Terraform speculative plan
	cd terraform && terraform plan

.PHONY: tf-apply
tf-apply: ## Apply Terraform infrastructure changes
	cd terraform && terraform apply -auto-approve

.PHONY: k8s-apply
k8s-apply: ## Apply raw Kubernetes manifests
	kubectl apply -f k8s/

.PHONY: k8s-delete
k8s-delete: ## Delete Kubernetes resources
	kubectl delete -f k8s/

.PHONY: helm-lint
helm-lint: ## Validate Helm chart syntax and template rendering
	helm lint helm/cloudops-nexus
	helm template test-release helm/cloudops-nexus > /dev/null

.PHONY: helm-deploy
helm-deploy: ## Deploy application via Helm chart
	helm upgrade --install $(APP_NAME) helm/cloudops-nexus -n cloudops --create-namespace
