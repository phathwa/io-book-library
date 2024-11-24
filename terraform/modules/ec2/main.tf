resource "aws_instance" "web" {
  count                       = length(var.ec2_names)
  ami                         = "ami-0658158d7ba8fd573" # Amazon Linux 2 AMI
  instance_type               = "t3.micro"
  associate_public_ip_address = true
  vpc_security_group_ids      = [var.sg_id]
  subnet_id                   = var.subnets[count.index]
  availability_zone           = data.aws_availability_zones.available.names[count.index]
  iam_instance_profile        = aws_iam_instance_profile.ec2_instance_profile.name


  user_data = <<-EOF
              #!/bin/bash
              echo "************************************************"
              echo -e "\npreparing environment....."

              # Install Python, pip, git, and AWS CLI (CLI to make sure)
              yum install -y python3 python3-pip git aws-cli jq

              # Clone Flask app from GitHub
              cd /home/ec2-user
              git clone https://github.com/phathwa/io-book-library
              cd io-book-library

              # Install Flask and required dependencies
              python3 -m venv .venv
              source .venv/bin/activate 
              pip3 install -r requirements.txt

              # Retrieve secret from AWS Secrets Manager
              REGION="${var.region}"
              SECRET=$(aws secretsmanager get-secret-value --region $REGION --secret-id "${var.secret_name}" --query SecretString --output text)

              if [ $? -ne 0 ]; then
                  echo "Failed to retrieve secret"
                  exit 1
              fi

              # Extract API key from the secret
              API_KEY=$(echo $SECRET | jq -r '.["x-api-key"]')
              if [ -z "$API_KEY" ]; then
                  echo "API_KEY not found in secret"
                  exit 1
              fi

              echo "export API_KEY=$API_KEY" >> /etc/profile

              # Extract Database URI from the secret
              DATABASE_URI=$(echo $SECRET | jq -r '.["database-uri"]')
              if [ -z "$DATABASE_URI" ]; then
                  echo "DATABASE_URI not found in secret"
                  exit 1
              fi

              echo "export DATABASE_URI=$DATABASE_URI" >> /etc/profile

              # Set Flask environment variable
              echo "export FLASK_ENV=production" >> /etc/profile
              
              # Apply the environment variables
              source /etc/profile

              # Start application
              echo "starting application........"
              nohup python3 main.py > /var/log/io-library-app.log 2>&1 &
            EOF

  tags = {
    Name = var.ec2_names[count.index]
  }
}

resource "aws_iam_role" "ec2_role" {
  name = "ec2-secrets-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Effect    = "Allow"
      }
    ]
  })
}

resource "aws_iam_policy" "secrets_access_policy" {
  name = "SecretsManagerAccessPolicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = var.secret_arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "role_policy_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.secrets_access_policy.arn
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2-instance-profile"
  role = aws_iam_role.ec2_role.name
}
