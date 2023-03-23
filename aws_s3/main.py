"""
Main file that does the whole process
"""

from listing_all_files import *

bucket_name = "pub-rss-feed-store"


def main():
    # New dict that contains new pub dict with only unique files
    custom_pub_dict = {}
    updates = False

    if not updates:
        all_pubs_dict = read_dict('file_content')
        new_dict = {}

        i = 0
        print("Doing manipulation")
        for k in all_pubs_dict:
            new_dict[k] = all_pubs_dict[k]
            i += 1

            if i == 5:
                break

        all_pubs_dict = new_dict

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
        for key in custom_pub_dict[pub]:
            writing_to_s3_custom(key)

    print("******************************************************")
    print("Completed copying new files to new folder")
    print("******************************************************")

    return custom_pub_dict



result = main()

print(result)

with open('main_results', 'w') as file:
    file.write(str(result))

