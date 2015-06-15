#!/usr/bin/python
#
# The purpose of this script is to update the dns with a new elb
#
import boto.route53
import logging
from lib import conn_dns

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def update_dns(app, environment, elb, zone):
    """update rout53 with new elb"""
    a_name = "{0}-{1}.{2}".format(environment, app, zone)
    print a_name
    a = update_a(
        name=a_name,
        value=elb,
        ttl=300,
        identifier=None,
        comment='')
    conn_dns.zone(a)
    return ag
