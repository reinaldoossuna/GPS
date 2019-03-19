# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.2
#   kernelspec:
#     display_name: Python [conda env:ic] *
#     language: python
#     name: conda-env-ic-py
# ---

from netCDF4 import Dataset, num2date
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import os
from pathlib import Path

# SE NAO TIVER O NETCDF rode essa celula
# 
# !conda install -y -c conda-forge netcdf4

path_corr = "DATA/GRACE/CLM4.SCALE_FACTOR.DS.G300KM.RL05.DSTvSCS1409.nc"
corr = Dataset(path_corr,mode='r')
corr

data_path = Path("DATA/GRACE/")
grace_data = list(data_path.glob("GRCTellus*"))
grace_data

nc = Dataset(grace_data[0], mode="r")
nc

nc.variables.keys()

lat_gleam = nc.variables['lat']
lon_gleam = nc.variables['lon']
time_gleam = nc.variables['time']
lwe_thickness_gleam = nc.variables['lwe_thickness']

lat_gleam, lat_gleam[:]

time_units_gleam = nc.variables['time'].units
print(time_units_gleam)

date_gleam = num2date(time_gleam[:], time_units_gleam)
date_gleam[:5]

# +

plt.pcolormesh(lon_gleam[:],lat_gleam[:], lwe_thickness_gleam[0])
plt.colorbar()
plt.show()
