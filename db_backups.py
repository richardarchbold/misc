#!/usr/bin/python

# small python script to take DB backups once per day when the laptop is on

# check to see if /home/richard/Documents/CollegeProject/database/backups/DATE.sql.gz exist
# if it does, cool, just exit
# if it does not, check to see if mysql is running, and if it is, run the backup

import subprocess
import os
import time

my_debug = 0

# create a date variable
today = time.strftime("%Y-%m-%d")

# setup all other backups file location variables.
base = "/home/richard/Documents/CollegeProject/database/backups/"
desired_backup = base + today + ".sql"
desired_gzipped_backup = desired_backup + ".gz"

if my_debug == 1:
    print "base: %s" % base
    print "desired_backup: %s" % desired_backup
    print "desired_gzipped_backup: %s" % desired_gzipped_backup
    print "================================================"

if os.path.isfile(desired_gzipped_backup):
    # already done, nothing to do here, move along.
    if my_debug == 1: print "already done, nothing to do here, move along."
    exit(0)
elif os.path.isfile(desired_backup):
    # backup has been taken, but not zip'd
    if my_debug == 1:  print "File exists but is not gzip'd (%s), so I will attempt to gzip it" % desired_backup
    # subprocess.check_call(["tcpdump", "-c5", "-vvv", "-w", raw, "host", ip])
    subprocess.call(["gzip", desired_backup])
    if os.path.isfile(desired_gzipped_backup):
        if my_debug == 1: print "Success, file is now gzip'd"
else:
    command = "mysqldump -urichard -pf2nnyfax --single-transaction --all-databases > " + desired_backup
    subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    subprocess.call(["gzip", desired_backup])
    if os.path.isfile(desired_gzipped_backup):
        if my_debug == 1: print "Success, %s is now gzip'd" % desired_gzipped_backup