# Query the existing secret
data "aws_secretsmanager_secret" "existing_secret" {
  name = var.secret_name
}

# Create the secret only if it doesn't exist
resource "aws_secretsmanager_secret" "this" {
  count = length(try(data.aws_secretsmanager_secret.existing_secret.id, "")) == 0 ? 1 : 0

  name        = var.secret_name
  description = "My API key for accessing service X"
}

# Create a secret version if the secret exists or is newly created
resource "aws_secretsmanager_secret_version" "this" {
  count = length(aws_secretsmanager_secret.this) > 0 ? 1 : 0

  secret_id     = length(aws_secretsmanager_secret.this) > 0 ? aws_secretsmanager_secret.this[0].id : try(data.aws_secretsmanager_secret.existing_secret.id, "")
  secret_string = jsonencode({
    API_KEY = var.secret_value  # Use the secret value passed as a variable
  })
}

# Output the secret ARN
output "secret_arn" {
  value = coalesce(
    try(data.aws_secretsmanager_secret.existing_secret.arn, null),
    length(aws_secretsmanager_secret.this) > 0 ? aws_secretsmanager_secret.this[0].arn : null
  )
}
