variable "vpc_cidr" {
  description = "CIDR range for VPC"
  type        = string
}

variable "environment" {
  description = "Environment identifier"
  type        = string
}

variable "availability_zones" {
  description = "Availability zones to deploy subnets"
  type        = list(string)
}

variable "cluster_name" {
  description = "Name of EKS cluster for subnet tagging"
  type        = string
}
