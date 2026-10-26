# Week 05 write up
### Concepts: VPCs, public and private subnets, route tables, internet gateways, and bastion hosts.

This week, I created a custom VPC with the CIDR block 10.0.0.0/16, using public and private subnets. I launched a bastion EC2 instance in a public subnet and a second EC2 instance in a private subnet. The bastion lets me access the private instance without giving that instance a public IP.

From WSL on my laptop, I connected to the bastion's Elastic IP using SSH on port 22. This traffic travels over the internet and through the VPC's internet gateway. The public subnet uses a default route to the internet gateway, and the bastion's security group allows SSH from my public IP. From the bastion, I then connected to the private instance at 10.0.141.178. This second connection stays within the VPC using its local route. The private instance's security group allows SSH only from the bastion's security group. A NAT gateway is not needed for this SSH connection.

One issue I ran into was a permission denied error when connecting from the bastion to the private instance. I needed to load my key into the SSH agent in WSL using ssh-add, then reconnect to the bastion with ssh -A. This allowed the private instance to authenticate through my local agent while keeping the private key on my laptop.
