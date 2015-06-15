#!/usr/bin/python
"""
Creates and configures ELB
"""
import boto.ec2.elb
from boto.ec2.elb.attributes import ConnectionDrainingAttribute
from boto.ec2.elb.attributes import CrossZoneLoadBalancingAttribute
from boto.ec2.elb.attributes import AccessLogAttribute
import logging
from lib import elb

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def create_elb(elb_name, az_list, ports):
    """Creates the ELB"""
    lb = elb.create_load_balancer(
        name=elb_name,
        zones=az_list,
        listeners=ports,
        subnets=None,
        security_groups=None,
        scheme='internet-facing',
        complex_listeners=None)
    return lb.name


def update_elb(lb_name):
    """Updates additional config for ELB"""
    elb.modify_lb_attribute(lb_name, 'crossZoneLoadBalancing', True)

    cda = ConnectionDrainingAttribute()
    cda.enabled = True
    cda.timeout = 90
    elb.modify_lb_attribute(lb_name, 'ConnectionDraining', cda)

    # this doesnt work yet, need to enable access logging to s3 bucket
    # ala = AccessLogAttribute()
    # ala.enabled = False
    # ala.s3_bucket_name = None
    # ala.s3_bucket_prefix = None
    # elb.modify_lb_attribute(lb, 'AccessLog', ala)

# def elb_health_check():
    # Add a custom health check here?


def check_elb():
    # lc_name
    elb_list = elb.get_all_load_balancers()
    return elb_list
