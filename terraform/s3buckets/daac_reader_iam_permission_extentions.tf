# NOTE: this is commented out for a few reasons
# 1) TF cannot arbitrarily in-place update trust relationship yet :shrug: even though boto3 has a call for this
# 2) it's frowned upon to use IaC to update these types of DAAC-approved IAM roles b/c when things get deleted
# they leave around AWS IDs that have to be deleted or can cause issues on updates. So it's encouraged
# to make these changes manually
# 3) leaving here so we know the EXACT policy additions we need

#data "aws_iam_role" "existing_daac_role" {
#  name = var.daac_reader_rolename
#}
#
##### add an entry for EMR to be trusted to assume the role
#resource "aws_iam_role_policy" "assume_role_policy" {
#  name   = "emr-serverless-assume-role"
#  role   = data.aws_iam_role.existing_daac_role.id
#
#  policy = jsonencode({
#    Version = "2012-10-17"
#    Statement = [
#      {
#        Effect = "Allow"
#        Principal = {
#          Service = "emr-serverless.amazonaws.com"
#        }
#        Action = "sts:AssumeRole"
#      }
#    ]
#  })
#}
#
##### add EMR inline policy to the existing daac role to do EMR things
#resource "aws_iam_policy" "emr_extra" {
#  name        = "EMR-Serverless-Extra-Policies"
#
#  policy = jsonencode({
#    Version = "2012-10-17"
#    Statement = [
#        {
#            "Effect": "Allow",
#            "Action": [
#                "logs:DescribeLogGroups"
#            ],
#            "Resource": [
#                "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
#            ]
#        },
#        {
#            "Effect": "Allow",
#            "Action": [
#                "logs:PutLogEvents",
#                "logs:CreateLogGroup",
#                "logs:CreateLogStream",
#                "logs:DescribeLogStreams"
#            ],
#            "Resource": [
#                "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/emr-serverless:*"
#            ]
#        },
#        {
#            "Effect": "Allow",
#            "Action": [
#                "s3:PutObject",
#                "s3:GetObject",
#                "s3:ListBucket",
#                "s3:DeleteObject"
#            ],
#            "Resource": [
#                "${aws_s3_bucket.output_bucket.arn}",
#                "${aws_s3_bucket.output_bucket.arn}/*"
#            ],
#        }
#    ]
#  })
#}
#
#resource "aws_iam_policy_attachment" "logging_policy_attachment" {
#  name       = "AttachEMRServerlessExtraPolicies"
#  roles      = [data.aws_iam_role.existing_daac_role.name]
#  policy_arn = aws_iam_policy.emr_extra.arn
#}