variable "region" {
  description = "The AWS region to use"
  type        = string
}

variable "sg_id" {
  description = "SG ID for EC2"
  type = string
}

variable "subnets" {
  description = "Subnets for EC2"
  type = list(string)
}

variable "ec2_names" {
    description = "EC2 names"
    type = list(string)
    default = ["io-lib-serv-1", "io-lib-serv-2"]
}
variable "secret_arn" {
  description = "The ARN of the AWS Secrets Manager secret"
  type        = string
}

variable "secret_name" {
  description = "The name of the secret stored in AWS Secrets Manager"
  type        = string
}


