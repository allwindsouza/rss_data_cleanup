import boto3
import configparser
import csv
import ast
import xml_util
import xml_diff

old_bucket_name = "pub-rss-feed-store"
new_bucket_name = "test-automation-compass"
local = True

if local:
    config = configparser.ConfigParser()
    config.read('/home/allwind/Desktop/CAS/rss_data_cleanup/aws_s3/config.ini')

    access_key = config['AWS']['aws_access_key_id']
    secret_key = config['AWS']['aws_secret_access_key']
    session_token = config['AWS']['aws_session_token']

    s3 = boto3.resource('s3', aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        aws_session_token=session_token)

    bucket = s3.Bucket(new_bucket_name)

else:
    session = boto3.Session(profile_name="user")
    s3_resource = session.resource('s3')

    bucket = s3_resource.Bucket(new_bucket_name)


def writing_to_s3_custom(key):
    """
    sample inp: data, Rss_files_v2/86918/1673600864.2579598.xml
    """
    print(f"Old key: {key}")

    from hash_store import hash_dict
    keys = key.split("/")
    old_hash = keys[1]
    file_name = keys[2]

    new_key = f"ad_collection/{old_hash}/{file_name}"

    copy_source = {
        'Bucket': old_bucket_name,
        'Key': key
    }
    bucket.Object(new_key).copy_from(CopySource=copy_source)

    print(f"Wrote to s3 bucket: {old_bucket_name}, from Old_Key: {key}, to New_Key: {new_key}, "
          f"new_bucket: {new_bucket_name}")


def read_dict(path):
    with open(path, 'r') as file:
        data = file.read()
    data = ast.literal_eval(data)
    return data


def copy_only_x(x=15, folders=None):

    if folders is None:
        folders = []

    for folder in folders:
        counter = 0
        for obj in bucket.objects.filter(Prefix=f"Rss_v3/{folder}/"):
            key = obj.key
            writing_to_s3_custom(key)
            counter += 1
            if counter > x-1:
                break


copy_only_x() # give inputs and run this to populate kp bucket.

