provider "aws" {
  region = "eu-north-1"  # Replace with your desired region
}

# Fetch the secret from AWS Secrets Manager
data "aws_secretsmanager_secret" "my_secret" {
  name = "my-api-key-secret"  # The name of your secret in Secrets Manager
}

data "aws_secretsmanager_secret_version" "my_secret_version" {
  secret_id = data.aws_secretsmanager_secret.my_secret.id
}

# Launch an EC2 instance with the secret as an environment variable
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"  # Example AMI, replace with your own
  instance_type = "t2.micro"               # Example instance type

  # User data script to inject the secret as an environment variable
  user_data = <<-EOF
              #!/bin/bash
              export MY_API_KEY="${data.aws_secretsmanager_secret_version.my_secret_version.secret_string}"
              # Start your application, for example:
              # nohup python3 app.py &
              EOF

}

# Optionally, output the API key (useful for debugging)
output "api_key" {
  value = data.aws_secretsmanager_secret_version.my_secret_version.secret_string
  sensitive = true  # This will prevent the key from showing in the Terraform output
}
