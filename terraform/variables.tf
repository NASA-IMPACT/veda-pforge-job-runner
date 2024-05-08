variable "emr_name" {
  description = "The EMR cluster name"
  type        = string
}

variable "repository_name" {
  description = "The ECR repository name to be used by our EMR deployment"
  type        = string
}

variable "aws_region" {
  description = "The AWS region to create resources in"
  type        = string
  default     = "us-west-2"
}

variable "emr_release_label" {
  description = "The EMR release to build"
  type        = string
  default     = "emr-7.0.0"
}

variable "execution_role_template" {
  description = "Path to the template defining an EMR execution role to be created"
  type        = string
  default     = "./emr/execution_role.json.tpl"
}

variable "bucket_suffix" {
  description = "suffix to add to s3 buckets so they are unique"
  type        = string
}
