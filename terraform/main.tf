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
  source      = "./modules/ec2"
  sg_id       = module.sg.sg_id
  subnets     = module.vpc.subnet_ids
  secret_arn  = data.aws_secretsmanager_secret.existing_secret.arn
  secret_name = "io-library-secrets"  # Will key app secrets
  region      = var.region 
}


module "alb" {
  source = "./modules/alb"
  sg_id = module.sg.sg_id
  subnets = module.vpc.subnet_ids
  vpc_id = module.vpc.vpc_id
  instances = module.ec2.instances
}

# Query the Existing Secret (Read-Only)
data "aws_secretsmanager_secret" "existing_secret" {
  name = "io-library-secrets"  # The name of your existing secret
}

output "secret_arn" {
  value       = data.aws_secretsmanager_secret.existing_secret.arn
  description = "The ARN of the existing secret"
}

output "alb_dns_name" {
  value       = module.alb.alb_dns_name
  description = "The DNS name of the Application Load Balancer"
}



