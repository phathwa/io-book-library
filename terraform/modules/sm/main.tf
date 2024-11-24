# Query the existing secret
data "aws_secretsmanager_secret" "existing_secret" {
  name = var.secret_name
}

# Query the latest version of the secret value
data "aws_secretsmanager_secret_version" "existing_secret_version" {
  secret_id = data.aws_secretsmanager_secret.existing_secret.id
}

# Output the secret ARN
output "secret_arn" {
  value = data.aws_secretsmanager_secret.existing_secret.arn
}

# Output the secret value (optional, not recommended for sensitive information)
output "secret_value" {
  value = data.aws_secretsmanager_secret_version.existing_secret_version.secret_string
}
