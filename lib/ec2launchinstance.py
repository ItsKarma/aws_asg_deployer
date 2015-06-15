#!/usr/bin/python
from time import sleep
import boto.ec2
from lib import conn_ec2
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def launch_instance(app, environment, ami, key, instance_type, sg, version, bdm):
    instance_tag = "{0}-{1}-{2}".format(app, environment, version)
    logging.info(" Launching Instance: {0}".format(instance_tag))
    reservation = conn_ec2.run_instances(
        image_id=ami,
        key_name=key,
        instance_type=instance_type,
        block_device_map=bdm,
        security_groups=sg
    )
    for instance in reservation.instances:
        instance.add_tag(key='Name', value=instance_tag)
        instance.add_tag(key='ENV', value=environment)
        while instance.update() != "running":
            if instance.update() == "terminated":
                logging.error(" the instance terminated for an unknown reason")
                exit(1)
            logging.info(" still waiting for instance to launch...")
            sleep(5)
        logging.info("instance_id: {0}".format(instance.id))
        logging.info("instance_key_name: {0}".format(instance.key_name))
        logging.info("instance_ip_address: {0}".format(instance.ip_address))
        return [instance.ip_address, instance.id, instance.key_name]
