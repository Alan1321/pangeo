import os
from dotenv import load_dotenv
from trmm_lis import trmm_lis
from s3_read import s3_read

load_dotenv()
BASE_PATH = os.getenv('BASE_PATH')

trmm_list_files = s3_read("null","TRMM-LIS", BASE_PATH).get_paths()
otd_files = s3_read("null","OTD", BASE_PATH).get_paths()
isslis_files = s3_read("null","ISS_LIS", BASE_PATH).get_paths()
hs3 = s3_read("null","HS3", BASE_PATH).get_paths()

# /home/asubedi/Desktop/work/GHRCCLOUD-4222/trmm-lis   --> store TRMM-LIS here

trmm_lis = trmm_lis(trmm_list_files, "/home/asubedi/Desktop/work/GHRCCLOUD-4222/trmm-lis")


