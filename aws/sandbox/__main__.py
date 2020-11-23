"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# https://github.com/pulumi/pulumi-aws/blob/master/examples/alb-new-py/__main__.py
vpc = aws.ec2.Vpc("sandbox-vpc",
                  cidr_block="10.0.0.0/16",
                  enable_dns_hostnames=True,
                  enable_dns_support=True)

subnet = aws.ec2.Subnet("sandbox-subnet",
                        vpc_id=vpc.id,
                        cidr_block="10.0.1.0/24",
                        map_public_ip_on_launch=True)

group = aws.ec2.SecurityGroup("sandbox-security-group",
                              description='Enable SSH access',
                              vpc_id=vpc.id,  # reference VPC from above
                              ingress=[{'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0']}])

size = 't2.micro'
ami = aws.get_ami(most_recent="true",
                  owners=["137112412989"],
                  filters=[{"name": "name", "values": ["amzn2-ami-hvm-*"]}])

server = aws.ec2.Instance('sandbox-server',
                          instance_type=size,
                          subnet_id=subnet.id,  # !!! Without subnet_id instance creation fails (VPCIdNotSpecified)
                          vpc_security_group_ids=[group.id],    # reference security group from above
                          ami=ami.id
                          )

pulumi.export('publicIp', server.public_ip)
pulumi.export('publicHostName', server.public_dns)
