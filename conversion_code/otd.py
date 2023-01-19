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

class otd:
    def __init__(self, file_path, store_directory, var, type):
        self.paths = file_path
        self.directory = store_directory
        self.var = var
        self.type = type
        self.generate_cog()

    def generate_cog(self):
        if(self.type == "Full"):
            file = xa.open_dataset(self.paths[0], engine='pynio', decode_coords='all')
            grid = file[self.var]
            rows = grid.to_numpy()[:, :] == 0.
            grid.to_numpy()[rows] = None

            l = grid.coords['Latitude'].data
            l[0] = l[0] + 0.4
            l[len(l)-1] = l[len(l) - 1] - 0.4
            grid.coords['Latitude'] = l

            grid = grid.transpose('Latitude', 'Longitude')
            grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
            grid.rio.crs
            grid.rio.set_crs('epsg:4326', inplace=True)
            ds_type = grid.dims[0]
            cog_name = f'{self.var}_co.tif'
            cog_path = f"{self.directory}/{cog_name}"
            grid.rio.to_raster(rf'{cog_path}', driver='COG')
        else:
            for path in self.paths:
                file = xa.open_dataset(path, engine='pynio', decode_coords='all')
                print(file)
                flash_rate_ds = file[self.var]
                flash_rate_ds = flash_rate_ds.transpose(self.type, 'Latitude', 'Longitude')
                grids = []
                ds_type = flash_rate_ds.dims[0]

                for grid in flash_rate_ds:
                    grid_index = grid.coords[ds_type].values

                    # need to update the last latitude data for this COG to be converted
                    l = grid.coords['Latitude'].data
                    l[0] = l[0] + 0.4
                    l[len(l)-1] = l[len(l) - 1] - 0.4
                    grid.coords['Latitude'] = l

                    grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
                    grid.rio.crs
                    grid.rio.set_crs('epsg:4326', inplace=True)
                    
                    # Individual COGs are stored in a folder

                    cog_name = f'{self.var}_{ds_type}_{grid_index}_co.tif'
                    cog_path = f"{self.directory}/{cog_name}"
                    grid.rio.to_raster(rf'{cog_path}', driver='COG')
            
