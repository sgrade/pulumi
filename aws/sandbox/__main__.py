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
                          ami=ami.id,
                          # key_name="roman-dev"
                          )

# ssh_key = aws.ec2.KeyPair("roman-dev",
#                           public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDs7shf1gXPP6DwUiWQIiI3wdrnTx/4/lxD3cWr/wVyNJeiyBsN/HOxAQVe1k7LYU6Klt1tsF98AgAeKeE/9s/HmgAOQJLdhLlDk4Tvs7jMDwvwdvCj/rJoIIen1vdsYF44KlWarUVDJikR8TPSS/vRL5xp+rnztaWQWPezxYi0uXCZEuqqHNXt3GzlEHs1m1NAyUPTjc0HuX3ASiXsbD4MQtQxdVOwLwX/0JdqQkcdf97BjhBfmH0sBRXPZcPK694r5l5wK6W2pxZJEs+phDfvUUXtxhVj/N6G38yA3mDlwhG1jO3TKfL3LMMV7wlOMm7qIEWMRoekI0n+ea+olrRJQX+lG7Ww4Fcsayl1Un6hMHOgXXzpZnODFPp96NooDXoditnqhejWArSOREkNk4n6BCqDoiz9PVyisaX/idwh3AeJ8rowsjx41f2D08s8BKhf3Z9eSbXW5R/pp1ZONzCaB50NUVk1J8bZzpLDeGNKoeh/O3zvKYEik+euK6zaiTU= roman@dev")

pulumi.export('publicIp', server.public_ip)
pulumi.export('publicHostName', server.public_dns)
