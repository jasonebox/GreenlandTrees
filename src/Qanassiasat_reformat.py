#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 06:55:47 2023

reformat Greenland Trees geodata

@author: jason box
"""

from datetime import datetime
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import date
import geopandas as gpd
from pyproj import Proj, transform
from PIL import Image
# from datetime import date
from datetime import timedelta
import ftplib
import calendar
from matplotlib.ticker import FormatStrFormatter

# ## change to your system's login name to change dir for local work
if os.getlogin() == 'jason':
    base_path = '/Users/jason/Dropbox/GT_Geodata/GreenlandTrees/'
os.chdir(base_path)

def outputx(sentence_list,year):
    sentence_list=np.array(sentence_list)
        
    out=pd.DataFrame({
        'date':sentence_list[:,0].astype(str),
        'species':sentence_list[:,1].astype(str),
        'height':sentence_list[:,2].astype(float),
        'ID':sentence_list[:,3].astype(str),
        'lat':sentence_list[:,4].astype(float),
        'lon':sentence_list[:,5].astype(float),
        'elev':sentence_list[:,6].astype(float),
        'notes':sentence_list[:,7].astype(str),
                      })
    
    # format float
    vals=['lat','lon']
    for val in vals:
        out[val] = out[val].map(lambda x: '%.4f' % x)
    
    # format elev
    vals=['elev']
    for val in vals:
        out[val] = out[val].map(lambda x: '%.0f' % x)
        
    
    out=out.sort_values('ID')

    print(out)
    
    out.to_excel('./geodata/'+year+'_Qanassiasat_GreenlandTrees.xlsx')
    out.to_csv('./geodata/'+year+'_Qanassiasat_GreenlandTrees.csv')
    
# ---------------------------------------------------------------------- 2021
year='2021'
fn='/Users/jason/Dropbox/GT_Geodata/GT2021/GT 2021 geodata - Qann 2021.tsv'
df=pd.read_csv(fn, sep='\t')

print(df.columns)

temp=df.Position.values

sentence_list=[]

for i,t in enumerate(temp):
    t=str(t)
    t=t.replace('° ',',')
    t=t.replace("' W",',')
    t=t.replace("'",'')
    t=t.replace("N",'')
    if t.split(',')[0]!='nan':
        latdeg=int(t.split(',')[0])
        latmin=float(t.split(',')[1])
        lat=latdeg+latmin/60
        londeg=int(t.split(',')[2])
        lonmin=float(t.split(',')[3])
        lon=londeg+lonmin/60
        elev=float(str(df['Elevation'][i]).replace(' ft',''))/3.2804
        datex=pd.to_datetime(df.date[i]).strftime('%Y/%b/%d')
        species=str(df['tree type'][i])
        species=species.replace('Birch','betula')
        species=species.replace('Sitka spruce','sitchensis')
        sentence=datex,species,df['height'][i],df['GPS ID'][i],lat,lon,elev,df['source'][i]
        sentence_list.append(sentence)

        # print(lat,lon,datex)#elev,df['tree type'][i],df['height'][i])

outputx(sentence_list,year)

#%%

# ---------------------------------------------------------------------- 2022
year='2022'
import gpxpy
import pandas as pd

df=pd.read_csv('/Users/jason/Dropbox/GT_Geodata/GT2022/GT TT DT trees planted - heights_2022.csv')
print(df.columns)
df_namex=df.number.astype(str).values
df_namexx=[]
for nam in df_namex:
    nam=nam.zfill(3)
    # print(nam)
    df_namexx.append(nam)
# len(df)
df_namex=np.array(df_namexx)

# Load gpx.
gpx_path = '/Users/jason/Dropbox/GT_Geodata/GT2022/Qanassiasat-2022.GPX'
with open(gpx_path) as f:
    gpx = gpxpy.parse(f)

sentence_list=[]

# len(gpx.waypoints)

for i,waypoint in enumerate(gpx.waypoints):
    # print(waypoint)
    
    elev=waypoint.elevation
    datex=pd.to_datetime(waypoint.time).strftime('%Y/%b/%d')
    species=''
    namex=waypoint.name
    namex=namex.replace('Qan220001','')
    namex=namex.replace('Qan22 ','')
    namex=namex.replace('Qan22','')
    namex=namex.replace('Qan 22','')
    namex=namex.replace('08060','')
    namex=namex.replace('Qan','')
    namex=namex.zfill(3)
    height=np.nan
    source1=''
    source2=''
    if sum(df_namex==namex)>0:
        v=np.where(df_namex==namex)
        # print(v[0][0])
        # print(i,namex)
        # print(i,v,len(v))
        if len(v)>0:
            v=v[0][0]
            height=df['height cm'].values[v]
            # source=df['name of planter'].values[v]
            # source=namex
            source1=df['number'].values[v]
            source2=df['name of planter'].values[v]
            species=df['type'].values[v]
            # print(namex,height,source)

    # source=0,namex
    sentence=datex,species,height,source1,waypoint.latitude,waypoint.longitude,elev,source2
    # sentence=datex,species,height,source,lat,lon,elev

    print(sentence)
    sentence_list.append(sentence)
    # print(sentence)
        # print(lat,lon,datex)#elev,df['tree type'][i],df['height'][i])

outputx(sentence_list,year)
