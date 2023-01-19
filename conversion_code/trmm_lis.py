import os
#read
import xarray as xa
import s3fs
##
from s3_read import s3_read

class TrmmLisRecipe:
    def __init__(self, file_path ,store_directory, var):
        self.paths = file_path
        self.directory = store_directory
        self.var = var
        self.generate_cog()

    def generate_cog(self):
        fs = s3fs.S3FileSystem(anon=False)
        for path in self.paths:
            with fs.open(path) as file:
                print("Starting File: " + path + " ....", end="")
                file = xa.open_dataset(file)
                flash_rate_ds = file[self.var]
                if self.var == 'VHRFC_LIS_FRD':
                    grid = flash_rate_ds[::-1] # Orientation is flipped to the correct position
                    rows = grid.to_numpy()[:, :] == 0.
                    grid.to_numpy()[rows] = None
                        
                    grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
                    grid.rio.crs
                    grid.rio.set_crs('epsg:4326')

                    cog_name = f'{self.var}_co.tif'
                    cog_path = f"{self.directory}/{cog_name}"
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

                        cog_name = f'{self.var}_{ds_type}_{grid_index}_co.tif'
                        cog_path = cog_path = f"{self.directory}/{cog_name}"
                        grid.rio.to_raster(rf'{cog_path}', driver='COG')
            print("Complete!!")