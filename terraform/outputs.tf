output "ecr_module_repository_url" {
  value       = module.ecr.repository_url
}

output "input_bucket_name" {
  value       = module.s3buckets.input_bucket_name
}
output "input_bucket_arn" {
  value       = module.s3buckets.input_bucket_arn
}
output "output_bucket_name" {
  value       = module.s3buckets.output_bucket_name
}
output "output_bucket_arn" {
  value = module.s3buckets.output_bucket_arn
}
