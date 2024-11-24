
module "vpc" {
  source      = "./modules/vpc"
  vpc_cidr    = var.vpc_cidr
  subnet_cidr = var.subnet_cidr
}

module "sg" {
  source = "./modules/sg"
  vpc_id = module.vpc.vpc_id
}

module "ec2" {
  source     = "./modules/ec2"
  sg_id      = module.sg.sg_id
  subnets    = module.vpc.subnet_ids
  secret_arn = data.aws_secretsmanager_secret.existing_secret.arn
  secret_name = "io-library-secrets"  # will key app secrets
  region     = var.region 
}

# Query the existing secret (read-only)
data "aws_secretsmanager_secret" "existing_secret" {
  name = "io-library-secrets"  # The name of your existing secret
}

output "secret_arn" {
  value       = data.aws_secretsmanager_secret.existing_secret.arn
  description = "The ARN of the existing secret"
}
