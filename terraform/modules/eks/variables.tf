variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "cluster_version" {
  description = "Kubernetes control plane version"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where EKS will be deployed"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for worker nodes"
  type        = list(string)
}

variable "instance_types" {
  description = "EC2 instance types for managed node group"
  type        = list(string)
}

variable "min_capacity" {
  description = "Minimum node group scaling capacity"
  type        = number
}

variable "max_capacity" {
  description = "Maximum node group scaling capacity"
  type        = number
}

variable "desired_capacity" {
  description = "Desired node group scaling capacity"
  type        = number
}
