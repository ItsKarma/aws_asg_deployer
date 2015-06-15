import boto.ec2
import boto.ec2.elb
import boto.ec2.autoscale
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
import boto.route53

conn_ec2 = boto.ec2.connect_to_region('us-east-1')
elb = boto.ec2.elb.connect_to_region('us-east-1')
conn_as = AutoScaleConnection()
conn_dns = boto.route53.connect_to_region('us-east-1')
