terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.16.1"
    }
  }

  # backend "s3" {
  #   bucket = "/dev_backet"
  #   key    = "terraform.tfstate"
  #   region = "eu-north-1"
  # }
}

provider "aws" {
  region = var.region  # This uses the 'region' variable declared earlier
}