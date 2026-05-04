terraform {
  backend "s3" {
    bucket         = "demo-cicd-tofu-state-bd7820b6"
    key            = "banking-pipeline/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "demo-cicd-tofu-locks"
    encrypt        = true
  }
}
