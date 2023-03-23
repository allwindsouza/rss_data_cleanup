import csv
import os
import requests
import time
import shutil
import sys
from tempfile import NamedTemporaryFile
import logging
import datetime
import boto3
import hashlib
from pytz import timezone
import configparser

#
local = False

bucket_name = "pub-rss-feed-store"

if local:
    config = configparser.ConfigParser()
    config.read('/home/allwind/Desktop/CAS/rss_data_cleanup/aws_s3/config.ini')

    access_key = config['AWS']['aws_access_key_id']
    secret_key = config['AWS']['aws_secret_access_key']
    session_token = config['AWS']['aws_session_token']

    s3 = boto3.resource('s3', aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        aws_session_token=session_token)

    bucket = s3.Bucket(bucket_name)

else:
    session = boto3.Session(profile_name="user")
    s3_resource = session.resource('s3')

    bucket = s3_resource.Bucket(bucket_name)

# objects = s3.Bucket(bucket_name).objects.all()  # Gives for all buckets in the folder

folder_name = 'Rss_files_v2/e35bd/'
objects = bucket.objects.filter(Prefix=folder_name)  # Gives all files in a particular folder

print("Sorting objects")
sorted_objects = sorted(objects, key=lambda obj: obj.last_modified)
print("Completed Sorting objects")

# Count the number of objects in each prefix (folder)
prefix_counts = {}
for obj in objects:
    print(f"obj: {obj.key}")
    prefix = '/'.join(obj.key.split('/')[:-1])
    print(f"Prefix: {prefix}")
    if prefix:
        prefix_counts[prefix] = prefix_counts.get(prefix, 0) + 1
        print(f"Adding counter 1 for prefix: {prefix}")

# Print the prefix and its corresponding count
for prefix, count in prefix_counts.items():
    print(f"{prefix}: {count}")
