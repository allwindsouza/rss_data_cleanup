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

path = "/home/allwind/Desktop/CAS/rss_data_cleanup/rss_list"

# hashlib.sha256(row['rss_url'].encode()).hexdigest()[:5]

hash_dict = {}

with open(path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        hash_first_5 = hashlib.sha256(row[0].encode()).hexdigest()[:5]
        hash_last = hashlib.sha256(row[0].encode()).hexdigest()[56:64]
        hash_dict[hash_first_5] = hash_last

print(hash_dict)

