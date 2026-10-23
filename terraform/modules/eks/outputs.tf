output "cluster_id" {
  description = "EKS cluster ID"
  value       = aws_eks_cluster.main.id
}

output "cluster_endpoint" {
  description = "Endpoint URL for Kubernetes API server"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = aws_eks_cluster.main.certificate_authority[0].data
}

output "oidc_provider_arn" {
  description = "ARN of the OIDC Provider for IAM Roles for Service Accounts"
  value       = aws_iam_openid_connect_provider.eks.arn
}

output "node_group_arn" {
  description = "ARN of the managed EKS node group"
  value       = aws_eks_node_group.main.arn
}
