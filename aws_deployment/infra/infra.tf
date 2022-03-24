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

######### VPC #########
resource "aws_vpc" "vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
  enable_classiclink   = "false"
  instance_tenancy     = "default"

  tags = {
    Name = "${var.app}-vpc"
  }
}

######### IGW #########
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.app}-igw"
  }
}

#################
# PUBLIC SUBNET #
#################

resource "aws_subnet" "public-subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = "true"
  availability_zone       = "eu-west-1a"
  tags = {
    Name = "${var.app}-public-subnet"
  }
}

#######################
# PUBLIC ROUTE TABLE #
#######################
resource "aws_route_table" "public-rt" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "${var.app}-public-rt"
  }
}

# Nat SG
resource "aws_security_group" "app-instance-sg" {
  name        = "allow_web"
  vpc_id      = aws_vpc.vpc.id
  description = "Allow inbound traffic"
  tags = {
    Name = "${var.app}-app-instance-sg"
  }
}

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

## SG Rule egress
resource "aws_security_group_rule" "web_egress_allow_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.app-instance-sg.id
}

## SG Rule ingress
resource "aws_security_group_rule" "ingress_allow_all" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = -1
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.app-instance-sg.id
}

##################################
# PUBLIC ROUTE TABLE ASSOCIATION #
##################################
resource "aws_route_table_association" "public-subnet" {
  subnet_id      = aws_subnet.public-subnet.id
  route_table_id = aws_route_table.public-rt.id
}