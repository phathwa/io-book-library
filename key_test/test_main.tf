# Fetch the environment variable
locals {
  test_api_key = getenv("TEST_API_KEY", "real-fake-key")  # Fallback to "default_value" if LOCAL_KEY is not set
}

resource "aws_secretsmanager_secret" "test_api_key" {
  name        = "test-api-key"
  description = "My API key for accessing service X"
}

resource "aws_secretsmanager_secret_version" "test_api_key_version" {
  secret_id     = aws_secretsmanager_secret.test_api_key.id
  secret_string = jsonencode({
    TEST_API_KEY = local.test_api_key
  })

  depends_on = [aws_secretsmanager_secret.test_api_key]  # Ensure secret is created first
}
# @TODO this looks like a better quicker solution