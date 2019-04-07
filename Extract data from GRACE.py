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
#     display_name: Python [conda env:ic]
#     language: python
#     name: conda-env-ic-py
# ---

from netCDF4 import Dataset, num2date
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import os
from pathlib import Path
import pandas as pd

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
# -

braz_lat= -15.9474753422
braz_long = 360 + -47.8778689831


def find_nearest(array, value,n=1):
    array = np.asarray(array)
    diff = np.abs(array - value)
    nearest = array[diff.argsort()][:n]
    idxs = []
    for i in range(n):
        idxs.append(np.where(array == nearest[i]))
    return np.sort(idxs)[::-1].flatten()


find_nearest(lat_gleam,braz_lat_long[0],4)


def make_mask(src,list_x,list_y):
    src = np.asarray(src)
    mask = np.full_like(src,False,dtype=bool)

    for x in list_x:
        for y in list_y:
            mask[x,y] = True
    return mask


list_x = find_nearest(lat_gleam,braz_lat_long[0],4)
list_y = find_nearest(lon_gleam,360+braz_lat_long[1],4)

lwe_thickness_gleam.shape

mask = make_mask(lwe_thickness_gleam[0],list_x,list_y)

mask

lwe_thickness_gleam[0][:].filled()[mask]


def get_mean_mask(matrix, mask):
    mean = matrix[:][mask].mean()
    return mean


get_mean_mask(lwe_thickness_gleam[0],mask)

# +
lista = []
for lwe_thickness in lwe_thickness_gleam:
    lista.append(get_mean_mask(lwe_thickness,mask))
    
lista


# -

def read_data(grace,lat,long,ns): 

    name = grace.as_posix()[21:24]
    
    nc = Dataset(grace, mode="r")
    
    lat_gleam = nc.variables['lat']
    lon_gleam = nc.variables['lon']
    time_gleam = nc.variables['time']
    lwe_thickness_gleam = nc.variables['lwe_thickness']
    
    time_units_gleam = nc.variables['time'].units
    
    date_gleam = num2date(time_gleam[:], time_units_gleam)
    
    dados = pd.DataFrame(index=date_gleam)
    

    for n in ns:
        name_column = name+"- %i" % n
        
        list_x = find_nearest(lat_gleam,lat,n)
        list_y = find_nearest(lon_gleam,long,n)

        mask = make_mask(lwe_thickness_gleam[0],list_x,list_y)
        column = []
        for lwe_thickness in lwe_thickness_gleam:
            column.append(get_mean_mask(lwe_thickness,mask))
        
        dados[name_column] = column
    
    
    return dados

dfs = []
for grace in grace_data:
    dfs.append(read_data(grace,braz_lat,braz_long,[2,3,4]))
df = pd.concat(dfs,sort=True)
df.sort_index(inplace=True)
df.head()

df = df.groupby(pd.Grouper(freq="M")).mean().dropna(how="all")


def get_df(graces,station):
    dfs = []
    lat = station[lat]
    long = station[long]
    for grace in grace_data:
        dfs.append(read_data(grace,lat,long,[2,3,4]))
    df = pd.concat(dfs,sort=True)
    df = df.groupby(pd.Grouper(freq="M")).mean().dropna(how="all")
    
    df.to_csv(station.name)



df.head()

df.mean(axis=1)


