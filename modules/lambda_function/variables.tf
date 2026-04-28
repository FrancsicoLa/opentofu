variable "function_name" {
  type        = string
  description = "Nombre de la Lambda"
}

variable "source_dir" {
  type        = string
  description = "Carpeta con el codigo Python"
}

variable "role_arn" {
  type        = string
  description = "ARN del rol IAM"
}

variable "timeout" {
  type    = number
  default = 10
}