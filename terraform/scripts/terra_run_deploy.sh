#!/bin/bash

# Function to log errors and stop execution if an error occurs
log_error() {
    echo "[ERROR] $1"
    exit 1
}

# Log the start of the deployment process
echo "************************************************"
echo "Starting Terraform deployment process..."

# Destroy existing infrastructure (if any)
echo "Destroying existing infrastructure..."
terraform destroy -auto-approve || log_error "Failed to destroy existing infrastructure."

# Initialize Terraform
echo "Initializing Terraform..."
terraform init || log_error "Failed to initialize Terraform."

# Validate the Terraform configuration
echo "Validating Terraform configuration..."
terraform validate || log_error "Terraform validation failed."

# Plan the deployment
echo "Planning Terraform deployment..."
terraform plan || log_error "Terraform plan failed."

# Apply the Terraform configuration
echo "Applying Terraform configuration..."
terraform apply -auto-approve || log_error "Terraform apply failed."

# Successful deployment
echo "Deployment completed successfully."
