import boto3
import configparser
import ast
from xml_util import compare_xml_files
from xml_diff import compare_xml_files


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
    session = boto3.Session(profile_name="s3-access-role")
    s3_resource = session.resource('s3')

    bucket = s3_resource.Bucket(bucket_name)

def get_all_folders_and_files(write_to_path=False):
    """
    Returns a dictionary that gives keys of all files in each of the rss folders.
    """
    folders = {}
    folder_name = 'Rss_files_v2/'
    objects = bucket.objects.filter(Prefix=folder_name)

    print("sorting the objects")
    sorted_objects = objects
    print("Completed sorting the objects")

    for obj in sorted_objects:
        k = obj.key
        k_split = k.split('/')
        print(k)
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


get_all_folders_and_files()
