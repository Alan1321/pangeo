#fix variable input

import os
import requests
import gzip
import shutil
from urllib.parse import urlparse
import sys
#read
import xarray as xa
import time
import numpy as np
# Mapping
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
##

class hs3:
    def __init__(self, file_path ,store_directory, var, type):
        self.path = file_path
        self.directory = store_directory
        #self.var = var
        self.var = 'Subset_Of_Stations'
        self.type = type
        self.generate_cog()

    def generate_cog(self):
        for path in self.path:
            try:
                start_time = time.time()
                print("---------------------------------------------------------------------------------------------------")
                print(f"Starting file: {path[-30:-1]}")
                #open file here
                file1 = xa.open_dataset(path, engine='netcdf4', decode_coords='all', decode_times=False)

                #lat, lon, data
                latitude = file1.Latitude.data
                longitude = file1.Longitude.data
                data = file1[self.var].data  

                full_dict = []
                for i in range(len(data)):
                    full_dict.append({
                        "latitude":latitude[i],
                        "longitude":longitude[i],
                        "data":data[i]
                })

                print("Full Dict Length: ", len(full_dict))

                if(len(full_dict) > 25000):
                    print(f"TOO_BIG_ERROR -- FILE: {self.path[-30:-1]} SIZE:{len(full_dict)}   .................")
                    print("---------------------------------------------------------------------------------------------------")
                    return

                #Sort geolocation here
                full_sorted_lat = np.sort(np.copy(latitude), axis=0)
                full_sorted_lon = np.sort(np.copy(longitude), axis=0)

                # split_sorted_lat = np.sort(np.copy(split_lat), axis=0)
                # split_sorted_lon = np.sort(np.copy(split_lon), axis = 0)

                #init grid here
                full_grid = np.zeros((len(latitude), len(latitude)))
                # split_grid = np.zeros((split_range, split_range))

                def find_full_lat_lon(lat, lon):
                    lat_index = None
                    lon_index = None
                    for i in range(len(full_sorted_lat)):
                        if(full_sorted_lat[i] == lat):
                            lat_index = i
                            break
                    for i in range(len(full_sorted_lon)):
                        if(full_sorted_lon[i] == lon):
                            lon_index = i
                            break
                    #print(lat_index, lon_index)
                    return [lat_index, lon_index]

                for di in full_dict:
                    index = find_full_lat_lon(di["latitude"], di["longitude"])
                    full_grid[index[0]][index[1]] = di["data"]

                new_xarray = xa.DataArray(
                data = full_grid,
                dims=("latitude", "longitude"),
                coords={
                    "latitude":full_sorted_lat,
                    "longitude":full_sorted_lon
                },
                attrs=dict(
                    description="",
                    units="",
                ),
                )

                new_xarray = new_xarray.transpose('latitude', 'longitude')
                new_xarray.rio.set_spatial_dims(x_dim='longitude', y_dim='latitude', inplace=True)
                new_xarray.rio.crs
                new_xarray.rio.set_crs('epsg:4326', inplace=True)

                print(path)
                cog_path = f'/home/asubedi/Desktop/pangeo/cog/{path[35:len(path)]}.tif'
                print(cog_path)
                new_xarray.rio.to_raster(rf'{cog_path}', driver='COG')

                print(f"Complete!! Time Taken: {time.time() - start_time}")
                print("---------------------------------------------------------------------------------------------------")
            except KeyboardInterrupt:
                sys.exit()
            else:
                print(f"Error {path}") 