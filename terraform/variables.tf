variable "vpc_cidr" {
  description = "VPC CIDR Range"
  type = string
}

variable "subnet_cidr" {
    description = "Subnet CIDRS"
    type = list(string)
}

variable "region" {
  description = "The AWS region to use"
  type        = string
  default     = "eu-north-1"  # Set a default region, or leave it empty for required input
}