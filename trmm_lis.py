import os
import requests
import gzip
import shutil
from urllib.parse import urlparse
#read
import xarray as xa
# Mapping
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
##
from s3_read import s3_read

class trmm_lis:
    def __init__(self, file_path ,store_directory):
        self.paths = file_path
        self.directory = store_directory
        self.generate_cog()

    def generate_cog(self):
        for path in self.paths:
            print("Starting File: " + path + " ....", end="")
            file = xa.open_dataset(path, engine='netcdf4', decode_coords='all')
            print("Error here")
            var = f'{path[4:9].upper()}_LIS_FRD'
            flash_rate_ds = file[var]

            if var == 'VHRFC_LIS_FRD':
                grid = flash_rate_ds[::-1] # Orientation is flipped to the correct position
                rows = grid.to_numpy()[:, :] == 0.
                grid.to_numpy()[rows] = None
                    
                grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
                grid.rio.crs
                grid.rio.set_crs('epsg:4326')

                cog_name = f'{var}_co.tif'
                cog_path = f"{self.store_directory}/{cog_name}"
                grid.rio.to_raster(rf'{cog_path}', driver='COG')
            else:
                ds_type = flash_rate_ds.dims[0]

                for grid in flash_rate_ds:
                    grid = grid[::-1] # Orientation is flipped to the correct position
                    rows = grid.to_numpy()[:, :] == 0.
                    grid.to_numpy()[rows] = None
                    grid_index = grid.coords[ds_type].values

                    grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
                    grid.rio.crs
                    grid.rio.set_crs('epsg:4326')

                    cog_name = f'{var}_{ds_type}_{grid_index}_co.tif'
                    cog_path = cog_path = f"{self.store_directory}/{cog_name}"
                    grid.rio.to_raster(rf'{cog_path}', driver='COG')
            print("Complete!!")

    def generate_full(self):
        pass
    def generate_regular(self):
        pass
    def store_cog(self):
        pass