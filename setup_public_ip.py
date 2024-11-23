import requests

def get_public_ip():
    """Fetch the public IP of the EC2 instance using IMDSv2."""
    try:
        # Step 1: Get the token
        token_url = "http://169.254.169.254/latest/api/token"
        token_headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        token_response = requests.put(token_url, headers=token_headers, timeout=5)
        token_response.raise_for_status()
        token = token_response.text

        # Step 2: Use the token to get the public IP
        metadata_url = "http://169.254.169.254/latest/meta-data/public-ipv4"
        metadata_headers = {"X-aws-ec2-metadata-token": token}
        response = requests.get(metadata_url, headers=metadata_headers, timeout=5)
        response.raise_for_status()
        
        public_ip = response.text
        return public_ip if public_ip else "No public IP assigned to this instance."
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching public IP: {e}"

if __name__ == "__main__":
    public_ip = get_public_ip()
    print(f"Public IP: {public_ip}")
