resource "aws_instance" "web" {
  count = length(var.ec2_names)
  ami           = "ami-0658158d7ba8fd573"
  instance_type = "t3.micro"
  associate_public_ip_address = true
  vpc_security_group_ids = [var.sg_id]
  subnet_id = var.subnets[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  user_data = <<-EOF
              #!/bin/bash
              # Install Python, pip and git
              yum install -y python3 python3-pip git

              # Clone Flask app from GitHub
              cd /home/ec2-user
              git clone https://github.com/phathwa/phathwa-book-library
              cd phathwa-book-library

              # Install Flask and required dependencies
              pip3 install -r requirements.txt
              
              # Export the public IP as an environment variable
              export PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
              echo "Public IP is: $PUBLIC_IP"


              # Run the Flask app on port 80
              nohup python3 main.py &  # Run Flask app in the background
            EOF
  tags = {
    Name = var.ec2_names[count.index]
  }
}