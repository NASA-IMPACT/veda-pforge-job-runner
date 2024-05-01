########## INPUT SCRIPT BUCKET ##################
resource "aws_s3_bucket" "input_bucket" {
  bucket = "veda-pforge-emr-input-scripts-${var.bucket_suffix}"

  tags = {
    Name        = "Veda PForge EMR Input Scripts"
  }
}

resource "aws_s3_bucket_policy" "input_bucket_policy" {
  bucket = aws_s3_bucket.input_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = [
          "s3:Get*",
          "s3:List*"
        ]
        Resource = [
          "${aws_s3_bucket.input_bucket.arn}",
          "${aws_s3_bucket.input_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_bucket_ownership_controls" "input" {
  bucket = aws_s3_bucket.input_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "input" {
  depends_on = [aws_s3_bucket_ownership_controls.input]

  bucket = aws_s3_bucket.input_bucket.id
  acl    = "private"
}

resource "aws_s3_object" "wrapper_script" {
  bucket = aws_s3_bucket.input_bucket.bucket
  key    = "runwrapper.py"
  source = "./runwrapper.py"
  etag = filemd5("./runwrapper.py")
}


########## PFORGE OUTPUT BUCKET ##################
resource "aws_s3_bucket" "output_bucket" {
  bucket = "veda-pforge-emr-outputs-${var.bucket_suffix}"

  tags = {
    Name        = "Veda PForge EMR Output Artifacts"
  }
}

resource "aws_s3_bucket_policy" "output_bucket_policy" {
  bucket = aws_s3_bucket.output_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = [
          "s3:*",
        ]
        Resource = [
          "${aws_s3_bucket.output_bucket.arn}",
          "${aws_s3_bucket.output_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_bucket_ownership_controls" "output" {
  bucket = aws_s3_bucket.output_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "output" {
  depends_on = [aws_s3_bucket_ownership_controls.output]

  bucket = aws_s3_bucket.output_bucket.id
  acl    = "private"
}
