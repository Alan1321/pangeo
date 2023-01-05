#fix var name, output path
import os
import requests
import gzip
import shutil
from urllib.parse import urlparse
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

class isslis:
    def __init__(self, file_path ,store_directory, var, type):
        self.paths = file_path
        self.directory = store_directory
        self.var = var
        self.generate_cog()

        self.lat_len
        self.lon_len
        self.npData
        self.lat
        self.lon
        
    def generate_cog(self):
        for fileName in self.paths:
            #global lat_len, lon_len, npData, lat, lon, files
            f2_var = 'lightning_area_density_index'
            file2 = xa.open_dataset(fileName, engine='netcdf4', decode_coords='all', decode_times=False)
            try:
                grid = file2.lightning_area_density_index
            except:
                print("Variable not found!!")
                return

            data = grid.data
            self.lat = np.copy(file2.lightning_area_density_index.lightning_area_lat.data)
            self.lon = np.copy(file2.lightning_area_density_index.lightning_area_lon.data)
            self.lat_len = len(grid.lightning_area_lat)
            self.lon_len = len(grid.lightning_area_lat)
            self.npData = np.zeros((self.lat_len, self.lon_len))

            sorted_lat = np.sort(self.lat, axis=0)
            sorted_lon = np.sort(self.lon, axis=0)
            npData2 = np.zeros((self.lat_len, self.lon_len))
            index = 0
            for i in range (self.lat_len):
                for j in range(self.lon_len):
                    if(i == j):
                        self.npData[i][j] = data[index]
                        index = index + 1
            #print(npData)
            for i in range(self.lat_len):
                for j in range(self.lon_len):
                    npData2[i][j] = self.get_value(sorted_lat[i], sorted_lon[j]) 
            
            finalFile = xa.DataArray(
                data = npData2,
                dims=("Latitude", "Longitude"),
                coords={
                    "Latitude":sorted_lat,
                    "Longitude":sorted_lon
                },
                attrs=dict(
                    description="Ambient temperature.",
                    units="degC",
                ),
            ) 
            finalFile = finalFile.transpose('Latitude', 'Longitude')
            finalFile.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
            finalFile.rio.crs
            finalFile.rio.set_crs('epsg:4326', inplace=True) 

            cog_name = f'{fileName[-38:-3]}.tif'
            cog_path = f'/home/asubedi/Desktop/pangeo/cog/{cog_name}'
            finalFile.rio.to_raster(rf'{cog_path}', driver='COG')

    def get_lat_index(self, lat_value):
        index = 0
        for i in range(self.lat_len):
            if(self.lat[index] == lat_value):
                return index
            else:
                index = index + 1

    def get_lon_index(self, lon_value):
        index = 0
        for i in range(self.lon_len):
            if(self.lon[index] == lon_value):
                return index
            else:
                index = index + 1

    def get_value(self, lat, lon):
        value = self.npData[self.get_lat_index(lat)][self.get_lon_index(lon)]
        return value