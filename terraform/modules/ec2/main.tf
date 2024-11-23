# Define the EC2 instance resource
resource "aws_instance" "web" {
  count                      = length(var.ec2_names)
  ami                        = "ami-0658158d7ba8fd573" # Amazon Linux 2 AMI
  instance_type              = "t3.micro"
  associate_public_ip_address = true
  vpc_security_group_ids     = [var.sg_id]
  subnet_id                  = var.subnets[count.index]
  availability_zone          = data.aws_availability_zones.available.names[count.index]
  iam_instance_profile       = aws_iam_instance_profile.ec2_instance_profile.name  # Attach IAM instance profile

  # User data script
  user_data = <<-EOF
              #!/bin/bash
              # Install Python, pip, git, and AWS CLI
              yum install -y python3 python3-pip git aws-cli

              # Clone Flask app from GitHub
              cd /home/ec2-user
              git clone https://github.com/phathwa/phathwa-book-library
              cd phathwa-book-library

              # Install Flask and required dependencies
              python3 -m venv .venv
              source .venv/bin/activate 
              pip3 install -r requirements.txt

              # Retrieve secret from AWS Secrets Manager
              SECRET_NAME="x-api-key"
              REGION="eu-north-1"
              SECRET=$(aws secretsmanager get-secret-value --region $REGION --secret-id $SECRET_NAME --query SecretString --output text)
              
              if [ $? -ne 0 ]; then
                echo "Failed to retrieve secret"
                exit 1
              fi

              echo "SECRET: $SECRET"  # Debugging; remove in production

              # Save the secret as an environment variable
              echo "export API_KEY=$SECRET" >> /etc/profile
              source /etc/profile

              # Run the Flask app on port 80
              nohup python3 main.py &
  EOF

  tags = {
    Name = var.ec2_names[count.index]
  }
}

# Define the IAM role for EC2
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

# Define the IAM policy for accessing AWS Secrets Manager
resource "aws_iam_policy" "secrets_access_policy" {
  name = "SecretsManagerAccessPolicy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "secretsmanager:GetSecretValue"
        Effect   = "Allow"
        Resource = var.secret_arn
      }
    ]
  })
}

# Attach the IAM policy to the role
resource "aws_iam_role_policy_attachment" "role_policy_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.secrets_access_policy.arn
}

# Create the IAM instance profile
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2-instance-profile"
  role = aws_iam_role.ec2_role.name
}

