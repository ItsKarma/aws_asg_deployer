#!/usr/bin/python
"""
Tasks for aws_asg_deployer
  create_elb
  create_launch_config
  create_asg
"""
import boto.ec2
from lib import ec2elbcreate
from lib import ec2launchconfig
from lib import ec2asg
from lib import ec2launchinstance
import sys
import argparse
import logging
from datetime import datetime
from ConfigParser import SafeConfigParser
from ConfigParser import RawConfigParser

cparser = SafeConfigParser()
cparser.read('config.ini')
rparser = RawConfigParser()
rparser.read('config.ini')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logging.addLevelName(logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
date = datetime.utcnow().strftime("%Y-%m-%dT%M-%S")

# take some command line arguments
# argparse overrides config file in next section
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--app", help="name of the application", type=str, choices=["create", "audit", "portal", "visp", "lql", "le"], required=True)
parser.add_argument("-e", "--env", help="environment: prod,staging,qa,dev", type=str, choices=["prod", "staging", "qa", "dev"])
parser.add_argument("-ver", "--version", help="code version - used for naming elb/lc/asg", type=str, required=True)
parser.add_argument("-s", "--snapshot-id", help="snapshot id - code is mounted here", type=str)
parser.add_argument("-i", "--instance-type", help="instance type", type=str)
parser.add_argument("--spot", help="if you want to launch a spot asg", action="store_true", default=False)
parser.add_argument("-p", "--spot-price", help="max spot price", type=float)
parser.add_argument("-sm", "--spot-min", help="min amount of instances in the spot asg", type=int)
parser.add_argument("-sx", "--spot-max", help="max amout of instances in the spot asg", type=int)
parser.add_argument("--ondemand", help="if you want to launch an ondemand asg", action="store_true", default=False)
parser.add_argument("-dm", "--ondemand-min", help="min amount of instances in the on-demand asg", type=int)
parser.add_argument("-dx", "--ondemand-max", help="max amout of instances in the on-demand asg", type=int)
parser.add_argument("-z", "--availability-zones", help="comma delimited list of availability zones", nargs='+', type=str)
args = parser.parse_args()

# assigning values from config.ini, override if argparse provided
app = args.app
environment = args.env
version = cparser.get('main', 'version')
if args.version:
    version = args.version
snapshot_id = cparser.get(app, 'snapshot_id')
if args.snapshot_id:
    snapshot_id = args.snapshot_id
instance_type = cparser.get('main', 'instance_type')
if args.instance_type:
    instance_type = args.instance_type
spot = rparser.getboolean('main', 'spot')
if args.spot:
    spot = args.spot
spot_price = cparser.get('main', 'spot_price')
if args.spot_price:
    spot_price = args.spot_price
spot_min = cparser.get('main', 'spot_min')
if args.spot_min:
    spot_min = args.spot_min
spot_max = cparser.get('main', 'spot_max')
if args.spot_max:
    spot_max = args.spot_max
ondemand = rparser.getboolean('main', 'ondemand')
if args.ondemand:
    ondemand = args.ondemand
ondemand_min = cparser.get('main', 'ondemand_min')
if args.ondemand_min:
    ondemand_min = args.ondemand_min
ondemand_max = cparser.get('main', 'ondemand_max')
if args.ondemand_max:
    ondemand_max = args.ondemand_max
availability_zones = cparser.get('main', 'availability_zones')
if args.availability_zones:
    availability_zones - args.availability_zones

# set some app vars
versiondash = version.replace('.', '-')
ami = cparser.get(app, 'ami')
key = cparser.get(app, 'key')
sg = [cparser.get(app, 'sg')]
ports = []
for (tmp_key, tmp_val) in cparser.items('elb'):
    port = []
    for item in tmp_val.split(','):
        try:
            port.append(int(item))
        except ValueError:
            port.append(item)
    ports.append(tuple(port))

# Set some nice names
elb_name = '{0}-elb-{1}-{2}'.format(environment, app, versiondash)
lc_spot_name = '{0}_lc_spot_{1}_{2}'.format(environment, app, version)
lc_ondemand_name = '{0}_lc_demand_{1}_{2}'.format(environment, app, version)
asg_spot_name = '{0}_asg_spot_{1}_{2}'.format(environment, app, version)
asg_demand_name = '{0}_asg_demand_{1}_{2}'.format(environment, app, version)

# set block device mapping (snapshot that has code)
ec2bdm = boto.ec2.blockdevicemapping
dev_sdf = ec2bdm.EBSBlockDeviceType(snapshot_id=snapshot_id)
bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
bdm['/dev/sdf'] = dev_sdf

# logging all vars
logging.info(" Stuffs:")
logging.info("  app: {0}".format(app))
logging.info("  environment: {0}".format(environment))
logging.info("  version: {0}".format(version))
logging.info("  snapshot_id: {0}".format(snapshot_id))
logging.info("  instance_type: {0}".format(instance_type))
logging.info("  spot: {0}".format(spot))
logging.info("  spot_price: {0}".format(spot_price))
logging.info("  spot_min: {0}".format(spot_min))
logging.info("  spot_max: {0}".format(spot_max))
logging.info("  ondemand: {0}".format(ondemand))
logging.info("  ondemand_min: {0}".format(ondemand_min))
logging.info("  ondemand_max: {0}".format(ondemand_max))
logging.info("  availability_zones: {0}".format(availability_zones))
logging.info("  date: {0}".format(date))
logging.info("  ports: {0}".format(ports))
logging.info(" More stuffs:")
logging.info("  versiondash: {0}".format(versiondash))
logging.info("  ami: {0}".format(ami))
logging.info("  key: {0}".format(key))
logging.info("  sg: {0}".format(sg))
logging.info("  elb_name: {0}".format(elb_name))
logging.info("  lc_spot_name: {0}".format(lc_spot_name))
logging.info("  lc_ondemand_name: {0}".format(lc_ondemand_name))
logging.info("  asg_spot_name: {0}".format(asg_spot_name))
logging.info("  asg_demand_name: {0}".format(asg_demand_name))
logging.info("  bdm (block device mapping): {0}".format(bdm))


def check_spot_ondemand(spot, ondemand):
    if spot is False and ondemand is False:
        logging.error(" spot and ondemand can't both be False!")
        exit(1)


def check_elb(elb_name):
    elb_resp = ec2elbcreate.check_elb()
    elb_list = list(elb_resp)
    for elb in elb_list:
        elb_str = str(elb).split(":")[1]
        if elb_str == elb_name:
            logging.error(" ELB: {0} already exists".format(elb_name))
            exit(1)


def lc_check(lc_spot_name, lc_ondemand_name, spot, ondemand):
    lc_resp = ec2launchconfig.check_launch_config()
    lc_list = list(lc_resp)
    logging.info(" lc_list: {0}".format(lc_list))
    if spot is True:
        for item in lc_list:
            item_str = str(item).split(":")[1]
            if item_str == lc_spot_name:
                logging.error(" Launch Config: {0} already exists".format(lc_spot_name))
                exit(1)
    if ondemand is True:
        for item in lc_list:
            item_str = str(item).split(":")[1]
            if item_str == lc_ondemand_name:
                logging.error(" Launch Config: {0} already exists".format(lc_ondemand_name))
                exit(1)


def create_availability_zone_list(azs):
    """converts the azs string into a list"""
    az_split = azs.split(',')
    az_list = []
    for az in az_split:
        az_list.append(az)
    logging.info("  az_list: {0}".format(az_list))
    return az_list


def launch_instance(app, environment, ami, key, instance_type, sg, version, bdm):
    """launch a single instance: dev"""
    instance_info = ec2launchinstance.launch_instance(app, environment, ami, key, instance_type, sg, version, bdm)
    print instance_info
    return instance_info


def main():
    # we only want to launch a single ondemand instance for dev
    if environment == "dev":
        launch_instance(app, environment, ami, key, instance_type, sg, version, bdm)
        exit()
    # make sure we are launching at least spot, ondemand, or both, but not None
    check_spot_ondemand(spot, ondemand)
    # lookup existing elb if already exists, exit
    check_elb(elb_name)
    # lookup existing launch configuration if already exists, exit
    # AutoScalingGroup can not exist without a Launch Configuration
    #  So we don't need to check if the ASG already exists.
    lc_check(lc_spot_name, lc_ondemand_name, spot, ondemand)
    # create list from availability_zones
    az_list = create_availability_zone_list(availability_zones)
    #
    # lookup existing ELB/LB/ASG
    # if group already exists, exit.
    #
    # create elb
    logging.info(" Creating ELB...")
    lb_name = ec2elbcreate.create_elb(elb_name, az_list, ports)
    logging.info(" Created ELB")
    # update elb
    logging.info(" Updating ELB with configs...")
    ec2elbcreate.update_elb(lb_name)
    logging.info(" ELB update finished")

    # create launch config
    if spot is True:
        logging.info(" Creating spot LaunchConfiguration...")
        lc = ec2launchconfig.create_spot_launch_config(lc_spot_name, ami, key, sg, instance_type, spot_price, bdm)
        logging.info(" Created spot LaunchConfiguration")
    if ondemand is True:
        logging.info(" Creating on-demand LaunchConfiguration...")
        lc = ec2launchconfig.create_demand_launch_config(lc_ondemand_name, ami, key, sg, instance_type, bdm)
        logging.info(" Created on-demand LaunchConfiguration")
    #
    # lookup existing asg
    # if group already exists, exit? or delete it?
    # script will error out if grou already esists
    #
    # create asg
    if spot is True:
        logging.info(" Creating spot AutoScalingGroup...")
        ec2asg.create_spot_asg(asg_spot_name, elb_name, lc_spot_name,
                               az_list, spot_min, spot_max, app)
        logging.info(" Created spot AutoScalingGroup")
    if ondemand is True:
        logging.info(" Creating demand AutoScalingGroup...")
        ec2asg.create_demand_asg(asg_demand_name, elb_name, lc_ondemand_name,
                                 az_list, ondemand_min, ondemand_max, app)
        logging.info(" Created demand AutoScalingGroup")
    #
    logging.info(" ELB/LaunchConfig/ASG Done")
    # return name of the elb to update the DNS
    logging.info(" ELB Name: {0}".format(elb_name))


if __name__ == "__main__":
    main()
