variable "app" {
  type    = string
  default = "fiability-back"
}

provider "aws" {
  region = "eu-west-1"
}

terraform{
  backend "s3" {
  }
}

####################################################################
# Get latest fiability-back AMI with given "Name" tag.
data "aws_ami" "app-ami" {
  owners = ["self"]
  filter {
    name   = "state"
    values = ["available"]

  }
  filter {
    name   = "tag:Name"
    values = ["fiability-back-ami"]
  }
  most_recent = true
}

# Get network resources
## VPC
data "aws_vpc" "vpc" {
  tags = {
    Name = "${var.app}-vpc"
  }
}

## Subnets

data "aws_subnet" "public-subnet" {
  tags = {
    Name = "${var.app}-public-subnet"
  }
}

## AZ
data "aws_availability_zones" "all" {}

data "aws_security_group" "app-instance-sg" {
  tags = {
    Name = "${var.app}-app-instance-sg"
  }
}

###############################
# fiability-back app instance #
###############################
resource "aws_instance" "app-instance" {
  ami                    = data.aws_ami.app-ami.id
  instance_type          = "t2.small"
  subnet_id              = data.aws_subnet.public-subnet.id
  security_groups        = [data.aws_security_group.app-instance-sg.id]
  source_dest_check      = "false"

  user_data = <<-EOT
    #!/bin/bash
    docker run -p 0.0.0.0:5000:5000/tcp start2015/fiability-back:latest
  EOT

  tags = {
    Name = "${var.app}-app-instance"
  }
}

output "app_instance_public_dns_name" {
  description = "Fiability-back app public DNS name"
  value       = aws_instance.app-instance.public_dns
}