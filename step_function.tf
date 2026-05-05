resource "aws_iam_role" "step_function_role" {
  name = "${var.project_name}-${var.student_id}-sfn-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "step_function_invoke_lambda" {
  name = "${var.project_name}-${var.student_id}-sfn-invoke"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "lambda:InvokeFunction"
        Effect = "Allow"
        Resource = [
          module.lambda_validate.function_arn,
          module.lambda_scan.function_arn,
          module.lambda_route.function_arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "step_function_invoke_attach" {
  role       = aws_iam_role.step_function_role.name
  policy_arn = aws_iam_policy.step_function_invoke_lambda.arn
}

resource "aws_sfn_state_machine" "banking_pipeline" {
  name     = "${var.project_name}-${var.student_id}-banking-pipeline"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    StartAt = "ValidateTransaction"
    States = {
      ValidateTransaction = {
        Type     = "Task"
        Resource = module.lambda_validate.function_arn
        Next     = "AssessRisk"
      }
      AssessRisk = {
        Type     = "Task"
        Resource = module.lambda_scan.function_arn
        Next     = "RouteTransaction"
      }
      RouteTransaction = {
        Type = "Choice"
        Choices = [
          {
            Variable     = "$.risk_level"
            StringEquals = "high"
            Next         = "HighRiskRoute"
          }
        ]
        Default = "LowRiskRoute"
      }
      HighRiskRoute = {
        Type     = "Task"
        Resource = module.lambda_route.function_arn
        End      = true
      }
      LowRiskRoute = {
        Type     = "Task"
        Resource = module.lambda_route.function_arn
        End      = true
      }
    }
  })
}
