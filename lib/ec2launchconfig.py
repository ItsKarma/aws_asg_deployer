#!/usr/bin/python
"""
Creates Launch Configuration
"""
import boto.ec2.autoscale
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
import logging
from datetime import datetime
from lib import conn_as

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
date = datetime.utcnow().strftime("%Y-%m-%dT%M-%S")


def create_spot_launch_config(lc_name, ami, key, sg, i_type, s_price, bdm):
    lc = LaunchConfiguration(
        name=lc_name,
        image_id=ami,
        key_name=key,
        security_groups=sg,
        user_data=None,
        instance_type=i_type,
        kernel_id=None,
        ramdisk_id=None,
        instance_monitoring=False,
        spot_price=s_price,
        block_device_mappings=[bdm],
        instance_profile_name=None)
    conn_as.create_launch_configuration(lc)
    return lc


def create_demand_launch_config(lc_name, ami, key, sg, i_type, bdm):
    lc = LaunchConfiguration(
        name=lc_name,
        image_id=ami,
        key_name=key,
        security_groups=sg,
        user_data=None,
        instance_type=i_type,
        kernel_id=None,
        ramdisk_id=None,
        instance_monitoring=False,
        block_device_mappings=[bdm],
        instance_profile_name=None)
    conn_as.create_launch_configuration(lc)
    return lc


def check_launch_config():
    lc_list = conn_as.get_all_launch_configurations()
    return lc_list
