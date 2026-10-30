terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 3.3"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }

  # Production S3 remote state backend configuration
  # backend "s3" {
  #   bucket         = "cloudops-nexus-tfstate"
  #   key            = "environments/production/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "cloudops-nexus-tflocks"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "CloudOps-Nexus"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "DevOps-Platform-Team"
    }
  }
}
