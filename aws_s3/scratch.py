import xml_util

from listing_all_files import *

# pub_dict = read_dict('/home/allwind/Desktop/CAS/rss_data_cleanup/aws_s3/file_content')

# Checking Rss_files_v2/86918/1673600864.2579598.xml and Rss_files_v2/86918/1673607676.431338.xml
# 	 downloading file: Rss_files_v2/86918/1673600864.2579598.xml
# 	 downloading file: Rss_files_v2/86918/1673607676.431338.xml


# for pub in pub_dict:
#     if len(pub_dict[pub]) >= 10 and len(pub) == len("b5696"):
#         file_1 = pub_dict[pub][0]
#         print(f"file 1: {file_1}")
#
#         file_2 = pub_dict[pub][1]
#         print(f"file 2: {file_2}")
#
#         data_1 = read_from_s3(file_1)
#         data_2 = read_from_s3(file_2)
#
#         print("Output")
#         try:
#             op = xml_util.compare_xml_files(data_1, data_2)
#             print(op)
#         except Exception as e:
#             print(f"Exce : {e}")


# data_1 = read_from_s3('Rss_files_v2/86918/1673600864.2579598.xml')
# data_2 = read_from_s3('Rss_files_v2/86918/1673607676.431338.xml')
#
# op = xml_util.compare_xml_files(data_1, data_2)
#
# print(op)


local = True
def main():
    # New dict that contains new pub dict with only unique files
    if local:
        all_pubs_dict = read_dict('/home/allwind/Desktop/CAS/rss_data_cleanup/aws_s3/file_content')

    else:
        # all_pubs_dict contains all pub_ids along with all the keys in that folder
        all_pubs_dict = get_all_folders_and_files(write_to_path='all_pubs_dict')

    print(f"Received all_pubs_dict with {len(all_pubs_dict)}")

    # Iterating through all the publisher folders
    pub = "86918"

    new_files = check_algo(all_pubs_dict[pub][:12])  # remove the [:12] part
    print(new_files)
    return new_files

main()

