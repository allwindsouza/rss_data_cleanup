"""
Listing all files folder wise, in last modified order.
"""

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
import ast
from xml_util import compare_xml_files
from xml_diff import compare_xml_files

config = configparser.ConfigParser()
config.read('/home/allwind/Desktop/CAS/Rss_collector/aws_s3/config.ini')

access_key = config['AWS']['aws_access_key_id']
secret_key = config['AWS']['aws_secret_access_key']
session_token = config['AWS']['aws_session_token']

s3 = boto3.resource('s3', aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    aws_session_token=session_token)

bucket_name = "pub-rss-feed-store"


def get_all_folders_and_files(write_to_path=False):
    """
    Returns a dictionary that gives keys of all files in each of the rss folders.
    """
    folders = {}
    folder_name = 'Rss_files_v2/'
    objects = s3.Bucket(bucket_name).objects.filter(Prefix=folder_name)

    print("sorting the objects")
    sorted_objects = sorted(objects, key=lambda obj: obj.last_modified)
    print("Completed sorting the objects")

    for obj in sorted_objects:
        k = obj.key
        k_split = k.split('/')

        if len(k_split) >= 3:
            print(k)
            if k_split[1] in folders:
                folders[k_split[1]].append(k)
            else:
                folders[k_split[1]] = [k]

    if write_to_path:
        with open('file_content', 'w') as file:
            file.write(str(folders))

    return folders


def read_dict(path):
    with open(path, 'r') as file:
        data = file.read()
    data = ast.literal_eval(data)
    return data


# for key in dict_data['dba35']:
#     print(key)

def read_from_s3(key, path=""):
    """
    Example key value:
    Rss_files_v2/dba35/1678979468.9394538.xml
    Rss_files_v2/dba35/1678980104.8269575.xml
    """
    print(f"\t downloading file: {key}")
    obj = s3.Object(bucket_name, key)
    data = obj.get()['Body'].read().decode('utf-8')

    if path:
        with open(path, 'w') as file:
            file.write(data)

    return data


result_list = []


def check_algo(pub_list: list):
    if len(pub_list) <= 10:
        return

    i = 0
    j = 1

    while j < len(pub_list):
        print(f"Checking {pub_list[i]} and {pub_list[j]}")
        if compare_xml_files(read_from_s3(pub_list[i]), read_from_s3(pub_list[j])):
            j += 1
            print("Almost same file")
        else:
            print("file is different")
            result_list.append(pub_list[i])
            i = j
            j = i + 1

    if i == 0:
        result_list.append(pub_list[i])

    print(result_list)
    print(f"Length of pub_list : {len(pub_list)}")
    print(f"Length of result_list : {len(result_list)}")

    return result_list


def writing_to_s3_custom(data, key):
    """
    sample inp: data, Rss_files_v2/86918/1673600864.2579598.xml
    """
    print(key)
    from hash_store import hash_dict
    keys = key.split("/")
    old_hash = keys[1]
    file_name = keys[2]

    new_hash = hash_dict.get(old_hash, old_hash)

    key = f"Rss_v3/{new_hash}/{file_name}"

    temp_file_name = "temp_file.txt"

    with open(temp_file_name, 'w') as new_file:
        new_file.write(data)
        print("\t Writing to file: {}.".format(key))

    # s3.upload_file(Filename=temp_file_name, Bucket=bucket_name, Key=key)
    print(f"Wrote to s3 bucket: {bucket_name}, Key: {key}")




writing_to_s3_custom("data", "Rss_files_v2/03eeb/1673600864.2579598.xml")


# dict_data = read_dict('file_content')
#
# check_algo(dict_data['dba35'][:20])


# print(read_from_s3("Rss_files_v2/dba35/1674296068.987057.xml"))

# ------------------------------
# data_1 = read_from_s3("Rss_files_v2/86918/1673600864.2579598.xml",
#                       "/home/allwind/Desktop/CAS/rss_data_cleanup/resource/file_01.xml")
# data_2 = read_from_s3("Rss_files_v2/86918/1673607676.431338.xml",
#                       "/home/allwind/Desktop/CAS/rss_data_cleanup/resource/file_02.xml")
#
# print("Output")
# try:
#     print(compare_xml_files(data_1, data_2))
# except Exception as e:
#     print(f"Exce : {e}")
