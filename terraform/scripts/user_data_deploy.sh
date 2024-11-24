#!/bin/bash
echo "************************************************"
echo -e "\nPreparing environment..."

# Function to log errors and stop execution if an error occurs
log_error() {
    echo "[ERROR] $1"
    exit 1
}

# Install Python, pip, git, AWS CLI, and jq
echo "Installing required packages..."
yum install -y python3 python3-pip git aws-cli jq || log_error "Failed to install required packages."

# Clone Flask app from GitHub
echo "Cloning Flask app from GitHub..."
cd /home/ec2-user || log_error "Failed to change directory to /home/ec2-user."
git clone https://github.com/phathwa/io-book-library || log_error "Failed to clone repository."
cd io-book-library || log_error "Failed to change directory to io-book-library."

# Install Flask and required dependencies
echo "Setting up virtual environment and installing dependencies..."
python3 -m venv .venv || log_error "Failed to create virtual environment."
source .venv/bin/activate || log_error "Failed to activate virtual environment."
pip3 install -r requirements.txt || log_error "Failed to install dependencies."

# Retrieve secrets from AWS Secrets Manager
echo "Retrieving secrets from AWS Secrets Manager..."
REGION="${var.region}"
SECRET=$(aws secretsmanager get-secret-value --region $REGION --secret-id "${var.secret_name}" --query SecretString --output text) || log_error "Failed to retrieve secrets."

API_KEY=$(echo $SECRET | jq -r '.["x-api-key"]') || log_error "Failed to extract API key from secret."
if [ -z "$API_KEY" ]; then
    log_error "API key not found in secret."
fi
echo "API_KEY retrieved successfully."

DATABASE_URI=$(echo $SECRET | jq -r '.["database-uri"]') || log_error "Failed to extract database URI from secret."
if [ -z "$DATABASE_URI" ]; then
    log_error "Database URI not found in secret."
fi
echo "DATABASE_URI retrieved successfully."

# Set environment variables
echo "Setting environment variables..."
echo "export API_KEY=$API_KEY" >> /etc/profile || log_error "Failed to set API_KEY environment variable."
echo "export DATABASE_URI=$DATABASE_URI" >> /etc/profile || log_error "Failed to set DATABASE_URI environment variable."
source /etc/profile || log_error "Failed to source environment variables."

# Start the application
echo "Starting application..."
nohup python3 main.py & || log_error "Failed to start application."

echo "Application started successfully."
