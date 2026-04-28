terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "quarantine" {
  bucket = "${var.project_name}-${var.student_id}"
  force_destroy = true
}

module "lambda_validate" {
  source = "./modules/lambda_function"

  function_name = "${var.project_name}-${var.student_id}-validate"
  source_dir    = "${path.module}/lambdas/validate_json"
  role_arn      = aws_iam_role.lambda_role.arn
}

module "lambda_scan" {
  source = "./modules/lambda_function"

  function_name = "${var.project_name}-${var.student_id}-scan"
  source_dir    = "${path.module}/lambdas/scan_content"
  role_arn      = aws_iam_role.lambda_role.arn
}

module "lambda_route" {
  source = "./modules/lambda_function"

  function_name = "${var.project_name}-${var.student_id}-route"
  source_dir    = "${path.module}/lambdas/route_file"
  role_arn      = aws_iam_role.lambda_role.arn
}
