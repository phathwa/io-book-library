terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.16.1"
    }
  }

  # backend "s3" {
  #   bucket = "terraform-remote-backend-s3"
  #   key    = "dev/terraform.tfstate"
  #   region = "eu-north-1"
  # }
}

provider "aws" {
  region = var.region  # This uses the 'region' variable declared earlier
}