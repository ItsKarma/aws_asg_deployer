aws_asg_deployer
=============
Python application to create a versioned ELB, Launch Configuration, and Auto-Scaling Group for a blue/green deployment with AWS using the Boto library.
If specified, two Auto-Scaling-Groups will be created, 1 spot, and 1 on-demand.

Setup:
-----------
* set environment variables
```
export AWS_ACCESS_KEY_ID=<aws_access_key_id>
export AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>
```
* Update config.ini with your settings, most can be overwritten by providing argument at command line (see usage)

Usage:
-----------
```
--app <string> (name of application to launch)
--env <string> (environment to launch the instances in)
--version <string> (code tag/version number, used for labeling)
--snapshot-id <string> (snapshot id of the volume to be mounted to /dev/sdf - code is here)
--instance-type <string> (instance type you want to launch)
--spot <bool> (do you want to launch a spot auto scaling group)
--spot-price <float> (max spot price to be allowed by the SPOT Launch Config, an ondemand instance will be launched if this is met)
--spot-min <int> (minimum amount of instances you want in the SPOT auto scaling group)
--spot-max <int> (maximum amount of instances you want in the SPOT auto scaling group)
--ondemand <bool> (do you want to launch an ondemand auto scaling group)
--ondemand-min <int> (minimum amount of instances you want in the ONDEMAND auto scaling group)
--ondemand-max <int> (maximum amount of instances you want in the ONDEMAND auto scaling group)
--availability-zones <string> (comma delimited list of AWS Availability Zones to launch instances in)
```

Example
```
python aws_asg_deployer.py --app web --env qa --tag 1.7.0 --instance-type c3.large --spot --spot-min 2 --spot-max 3 --ondemand --ondemand-min 2 --ondemand-max 3 --snapshot-id snap-936bc514 --spot-price 0.75 --availability-zones us-east-1a,us-east-1b,us-east-1c,us-east-1e
```

TO-DO
-----------
- Flip DNS (separate script)
- Create ScalingPolicy for ASG (http://boto.readthedocs.org/en/latest/autoscale_tut.html)
- Run the ec2-spot-instance-pricing script first to give us the instance_type and max values, then pass that into this script
