# Root Infrastructure Orchestration Module

module "vpc" {
  source = "./modules/vpc"

  vpc_cidr           = var.vpc_cidr
  environment        = var.environment
  availability_zones = var.availability_zones
  cluster_name       = var.cluster_name
}

module "eks" {
  source = "./modules/eks"

  cluster_name       = var.cluster_name
  cluster_version    = var.cluster_version
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids

  instance_types   = var.eks_node_instance_types
  min_capacity     = var.eks_min_capacity
  max_capacity     = var.eks_max_capacity
  desired_capacity = var.eks_desired_capacity

  depends_on = [module.vpc]
}
