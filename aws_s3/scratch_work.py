"""
Listing all files folder wise, in last modified order.
"""

import boto3
import configparser
import ast
import xml_util
import xml_diff

local = True

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

from hash_store import hash_store_v2

keys = hash_store_v2

values = keys.values()


def change_names(old_folder_name):
    old_folder_name = f"Rss_v3/{old_folder_name}/"
    for obj in bucket.objects.filter(Prefix=old_folder_name):
        old_key = obj.key
        old_folder = old_key.split("/")[1]
        file_name = old_key.split("/")[2]
        new_folder_name = hash_store_v2.get(old_folder, "null")

        if new_folder_name == "null":
            print("pass")
            continue

        # new_folder_name = "DELETE"  # remove this
        new_key = f"Rss_v3/{new_folder_name}/{file_name}"

        print(f"\t {new_key}")

        copy_source = {
            'Bucket': bucket_name,
            'Key': old_key
        }

        print(f"\t Writing file from {old_key} to {new_key}")
        bucket.Object(new_key).copy_from(CopySource=copy_source)

    print(f"********************Completed for {old_folder_name}***************************")


def change_all():
    # folders = set()
    # folder_prefix = "Rss_v3/"
    # for obj in bucket.objects.filter(Prefix=folder_prefix):
    #     key = obj.key
    #     folder_name = key.split("/")[1]
    #     if len(folder_name) <= 6:
    #         print(folder_name)
    #         folders.add(folder_name)

    folders = {'808e0', '54486', '86918', '0893c', 'cb662', 'ad23c', '690fb', 'e7e03', '27484', '2d185'}

    for old in folders:
        print(f"PROCESSING FOR {old}")
        change_names(old)

    print(folders)


# change_all()

# def read_dict(path):
#     with open(path, 'r') as file:
#         data = file.read()
#     data = ast.literal_eval(data)
#     return data
#
# dict_data = read_dict('file_content')
#
# print(dict_data.keys())

def get_all_folder():
    folders = set()
    folder_prefix = "Rss_v3/"
    objects = bucket.objects.filter(Prefix=folder_prefix)
    x = 208005
    print(f"Length of objects: {x}")
    count = 0
    for obj in objects:
        key = obj.key
        folder_name = key.split("/")[1]
        folders.add(folder_name)
        print(round((count/x)*100, 1), " %")
        count += 1

    print(folders)

# get_all_folder()

