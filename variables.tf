variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "demo-cicd-tofu"
}

variable "student_id" {
  description = "ID del estudiante"
  type        = string
}

variable "aws_region" {
  description = "Region de AWS"
  type        = string
  default     = "us-east-1"
}

