output "input_bucket_arn" {
  description = "The ARN of the S3 bucket input"
  value       = aws_s3_bucket.input_bucket.arn
}
output "input_bucket_name" {
  description = "The name of the input S3 bucket"
  value       = "s3://${aws_s3_bucket.input_bucket.bucket}"
}


output "output_bucket_arn" {
  description = "The ARN of the S3 bucket output"
  value       = aws_s3_bucket.output_bucket.arn
}
output "output_bucket_name" {
  description = "The name of the output S3 bucket"
  value       = "s3://${aws_s3_bucket.output_bucket.bucket}"
}