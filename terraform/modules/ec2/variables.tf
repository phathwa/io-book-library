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
    default = ["FlaskAPIServer1", "FlaskAPIServer2"]
}
variable "secret_arn" {
  description = "The ARN of the AWS Secrets Manager secret"
  type        = string
}