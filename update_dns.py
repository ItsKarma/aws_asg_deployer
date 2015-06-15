#!/usr/bin/python
"""
Tasks for update_dns:
  update_dns
"""
import sys
import argparse
import logging
from datetime import datetime
from lib import dns_update
from ConfigParser import SafeConfigParser

cparser = SafeConfigParser()
cparser.read('config.ini')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
date = datetime.utcnow().strftime("%Y-%m-%dT%M-%S")

# argparse overrides config file
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--app",
                    help="name of the application",
                    type=str,
                    choices=["create", "audit", "portal", "visp", "lql", "le"],
                    required=True)
parser.add_argument("-e", "--env",
                    help="environment: prod,staging,qa,dev",
                    type=str,
                    choices=["prod", "staging", "qa", "dev"],
                    required=True)
parser.add_argument("-l", "--elb",
                    help="",
                    type=str,
                    choices=["prod", "stage", "qa", "dev"],
                    required=True)
parser.add_argument("-z", "--zone",
                    help="route53 hosted zone",
                    type=str)
args = parser.parse_args()

# assigning values from config.ini, override if argparse provided
app = args.app
environment = args.env
zone = cparser.get('dns', 'zone')
if args.zone:
    zone = args.zone

# logging all vars
logging.info(" Stuffs:")
logging.info("  app: {0}".format(app))
logging.info("  environment: {0}".format(environment))
logging.info("  elb: {0}".format(elb))
logging.info("  zone: {0}".format(zone))

if __name__ == "__main__":
    dns_update.update(app, environment, elb, zone)
