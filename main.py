import os
# from dotenv import load_dotenv
# from trmm_lis import trmm_lis
from otd import otd
# from s3_read import s3_read
from local_read import local_read

# load_dotenv()
# BASE_PATH = os.getenv('BASE_PATH')

# trmm_lis_full = local_read("/home/asubedi/Desktop/raw-files/TRMM-LIS/FULL/").get_files()
# trmm_lis_monthly = local_read("/home/asubedi/Desktop/raw-files/TRMM-LIS/MONTHLY/").get_files()

# trmm_lis(trmm_lis_full, "/home/asubedi/Desktop/pangeo/cog/", "VHRFC_LIS_FRD")
# trmm_lis(trmm_lis_monthly, "/home/asubedi/Desktop/pangeo/cog/", "VHRMC_LIS_FRD")

otd_monthly = local_read("/home/asubedi/Desktop/raw-files/OTD/FULL/").get_files()
otd(otd_monthly, "/home/asubedi/Desktop/pangeo/cog/", "HRFC_COM_FR", "Full")