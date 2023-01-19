import os
from trmm_lis import TrmmLisRecipe

path = ["s3://lightning-dashboard-raw-files/TRMM-LIS/lis_vhrfc_1998_2013_v01.nc"] #testing trmm-lis-full 
path = ["s3://lightning-dashboard-raw-files/TRMM-LIS/lis_vhrmc_1998_2013_v01.nc"] #testing trmm-lis-monthly

trmm_lis_data = TrmmLisRecipe(path, "/home/asubedi/Desktop/pangeo/store", "VHRMC_LIS_FRD")
