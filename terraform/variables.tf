variable "aws_region" {
  description = "Target AWS region for deploying infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name (staging, production)"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["staging", "production", "dev"], var.environment)
    error_message = "Environment must be one of: staging, production, dev."
  }
}

variable "cluster_name" {
  description = "Name of the AWS EKS Kubernetes Cluster"
  type        = string
  default     = "cloudops-nexus-eks"
}

variable "cluster_version" {
  description = "Kubernetes control plane version"
  type        = string
  default     = "1.30"
}

variable "vpc_cidr" {
  description = "CIDR block for the Virtual Private Cloud (VPC)"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of AWS availability zones for high availability"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "eks_node_instance_types" {
  description = "EC2 instance types for EKS managed worker nodes"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "eks_min_capacity" {
  description = "Minimum number of worker nodes in autoscaling group"
  type        = number
  default     = 2
}

variable "eks_max_capacity" {
  description = "Maximum number of worker nodes in autoscaling group"
  type        = number
  default     = 6
}

variable "eks_desired_capacity" {
  description = "Desired number of worker nodes in autoscaling group"
  type        = number
  default     = 3
}
