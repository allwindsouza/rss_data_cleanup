"""
Main file that does the whole process
"""

from listing_all_files import *

config = configparser.ConfigParser()
config.read('config.ini')

access_key = config['AWS']['aws_access_key_id']
secret_key = config['AWS']['aws_secret_access_key']
session_token = config['AWS']['aws_session_token']

s3 = boto3.resource('s3', aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    aws_session_token=session_token)

bucket_name = "pub-rss-feed-store"
local = True


def main():
    # New dict that contains new pub dict with only unique files
    custom_pub_dict = {}

    if local:
        all_pubs_dict = read_dict('/home/allwind/Desktop/CAS/rss_data_cleanup/aws_s3/file_content')

    else:
        # all_pubs_dict contains all pub_ids along with all the keys in that folder
        all_pubs_dict = get_all_folders_and_files(write_to_path='all_pubs_dict')

    print(f"Received all_pubs_dict with {len(all_pubs_dict)}")

    # Iterating through all the publisher folders
    for pub in all_pubs_dict:
        print("Starting Iteration")
        # If any of the publisher folder contains more than 100 files, process only that file.
        if len(all_pubs_dict[pub]) >= 25:
            print(f"Starting to process for {pub} with length {len(all_pubs_dict[pub])}")
            new_files = check_algo(all_pubs_dict[pub][:12])  # remove the [:12] part

            print(f"Got custom files list for : {pub} with length {len(new_files)}")
            custom_pub_dict[pub] = new_files

            print("**************************************")
            print(f"Completed for {pub}, With num files: {len(custom_pub_dict[pub])}")
            print("**************************************")

        else:
            print("**************************************")
            print(f"Skipping for {pub}, because less files: {len(all_pubs_dict[pub])}")
            print("**************************************")

    print("--------------------------------------------------------")
    print("Completed Making new Pub Rss bucket")
    print("--------------------------------------------------------")

    for pub in custom_pub_dict:
        for key in pub[custom_pub_dict]:
            writing_to_s3_custom(key)

    print("******************************************************")
    print("Completed copying new files to new folder")
    print("******************************************************")

    return custom_pub_dict



result = main()

print(result)

with open('main_results', 'w') as file:
    file.write(str(result))

# all_pubs_dict = read_dict('/home/allwind/Desktop/CAS/rss_data_cleanup/aws_s3/file_content')
#
# x = all_pubs_dict['03eeb'][:12]
#
# print(check_algo(x))
