#!/bin/bash
# terraform destroy -auto-approve
terraform init
terraform validate
terraform plan
terraform apply -auto-approve