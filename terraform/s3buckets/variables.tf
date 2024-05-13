variable "input_bucket_name" {
  description = "Name of the input bucket used for scripts and tarballs of the runtime packages"
  type        = string
}

variable "output_bucket_name" {
  description = "Name of the output bucket where job artifacts/outputs go"
  type        = string
}

variable "account_id" {
  description = "aws account id for where buckets should exist"
  type        = string
}

variable "daac_reader_rolename" {
  # NOTE: this is currently disabled b/c it would be used for policy extensions on the DAAC-approved IAM role
  description = "the name of the role in the AWS account that everyone within that account assume to read from DAACs"
  type        = string
  default     = ""
}

variable "daac_reader_arn" {
  description = "the arn AWS account that everyone within that account assume to read from DAACs"
  type        = string
  default     = ""
}
