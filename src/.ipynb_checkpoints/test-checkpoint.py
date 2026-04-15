import xarray as xa

fname = "gfs.t06z.sfcanl.nc"
try:
    output = xa.open_dataset(fname, engine='netCDF4')
except Exception as e:
    print(e)
    raise e
print(output)