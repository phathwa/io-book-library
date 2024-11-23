module "vpc" {
  source     = "./modules/vpc"
  vpc_cidr   = var.vpc_cidr
  subnet_cidr = var.subnet_cidr
}

module "sg" {
  source = "./modules/sg"
  vpc_id = module.vpc.vpc_id
}

module "ec2" {
  source    = "./modules/ec2"
  sg_id     = module.sg.sg_id
  subnets   = module.vpc.subnet_ids
  secret_arn = module.sm.secret_arn  # Pass the secret ARN to EC2 module
}

module "sm" {
  source        = "./modules/sm"
  secret_name   = "x-api-key"  # Pass the secret name
  secret_value  = "real-key"  # Pass the secret value
}

resource "aws_iam_policy" "secrets_access_policy" {
  name        = "secrets-access-policy"
  description = "Allow access to Secrets Manager for the application"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = module.sm.secret_arn
      }
    ]
  })
}

output "secret_arn" {
  value       = module.sm.secret_arn
  description = "The ARN of the secret (existing or newly created)"
}
