#!/usr/bin/python
#
# The purpose of this script is to create a launch config and asg.
#
import boto.ec2.autoscale
from boto.ec2.autoscale import Tag
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
import logging
from datetime import datetime
from lib import conn_as

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
date = datetime.utcnow().strftime("%Y-%m-%dT%M-%S")


def create_spot_asg(asg_name, elb_name, lc_name, az_list, min, max, app):
    """create spot auto scaling group"""
    ag = AutoScalingGroup(
        name=asg_name,
        load_balancers=[elb_name],
        availability_zones=az_list,
        default_cooldown=180,
        launch_config=lc_name,
        desired_capacity=max,
        min_size=min,
        max_size=max,
        tags=[Tag(
            key='Name',
            value='aws-iad-portal-9.9.9-as-spot',
            propagate_at_launch=True,
            resource_id=asg_name),
            Tag(
            key='ENV',
            value='dev',
            propagate_at_launch=True,
            resource_id=asg_name)],
        # placement_group=???,
        # vpc_zone_identifier=???,
        termination_policies=['ClosestToNextInstanceHour'],
        connection=conn_as)
    conn_as.create_auto_scaling_group(ag)
    return ag


def create_demand_asg(asg_name, elb_name, lc_name, az_list, min, max, app):
    """create on-demand auto scaling group"""
    ag = AutoScalingGroup(
        name=asg_name,
        load_balancers=[elb_name],
        availability_zones=az_list,
        default_cooldown=180,
        launch_config=lc_name,
        desired_capacity=max,
        min_size=min,
        max_size=max,
        tags=[Tag(
            key='Name',
            value='aws-iad-portal-9.9.9-as-ondemand',
            propagate_at_launch=True,
            resource_id=asg_name),
            Tag(
            key='ENV',
            value='dev',
            propagate_at_launch=True,
            resource_id=asg_name)],
        # placement_group=???,
        # vpc_zone_identifier=???,
        termination_policies=['ClosestToNextInstanceHour'],
        connection=conn_as)
    conn_as.create_auto_scaling_group(ag)
    return ag
