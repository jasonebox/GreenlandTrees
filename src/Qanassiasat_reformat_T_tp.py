# -*- coding: utf-8 -*-
"""

Jason Box

"""
import os
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta


#https://strftime.org/

site='QANASIASSAT'

path='/Users/jason/Dropbox/Greenland Trees/GT_Geodata/GreenlandTrees/'
os.chdir(path)

files=['QANASIASSAT_UTC_2020-2021','QANASIASSAT_UTC_2021-2022']
# files=['QANASIASSAT_UTC_2020-2021']

for i,file in enumerate(files):
    #------------------------------------------------------------------ rain data
    if site == 'QANASIASSAT':
        fn="./precipitation_temperature_gauge/"+file+".csv"
        SN="20362477"
        epoch="20190830"
        timex="Date Time, GMT+00:00"
        if i==0:
            time_format='%m/%d/%y %I:%M:%S %p'
        else:
            time_format='%m/%d/%Y %I.%M.%S %p'

            
        # fn="./QAS_L/QAS_L_20180504/HOBO_rain_QAS_L-2016-2018.csv"
        # SN="10923288"
        # epoch="20180504"
        # timex="Date Time, GMT+00:00"
        # time_format='%m/%d/%y %I:%M:%S %p'
        
        # epoch='20200701'
        # fn='./QAS_L/QAS_L_20200701/QAS_L_20190828_20200701.hobo.csv'
        # SN='10923290'    
        # timex="Date Time, GMT+02:00"
        # time_format='%m/%d/%Y %I.%M.%S %p'
        
        site2=site
    
    
    df = pd.read_csv(fn,skiprows=2,names=['id','datex','T2m','event'])
    # print(df.columns)
    # print(df)
    
    
    df["time"]=pd.to_datetime(df.datex,format=time_format) 

    print()
    print(file)
    print('before')
    print(df["time"])
    
    df["time_UTC"]=df["time"]+timedelta(hours=2)

    print('after')
    print(df["time_UTC"])
    
    df["precip_mm_uncorrected"]=df["event"] * 0.2
    
    # year_rain=t_rain.dt.year
    # month_rain=t_rain.dt.month
    # day_rain=t_rain.dt.day
    # hour_rain=t_rain.dt.hour
    # min_rain=t_rain.dt.minute
    
    # #print(hour_rain)
    
    # n_rows_rain_data = len(ppt)
    
    if i==0:
        df["air_temperature_C"]= (df.T2m - 32) * 5/9.
        ppt_offset=np.nanmax(df["precip_mm_uncorrected"])
    else:
        df["air_temperature_C"]=df.T2m
        df["precip_mm_uncorrected"]+=ppt_offset
    
    # plt.plot(t_rain, ppt, linewidth=1,linestyle='-',color='r', label='QAS_L')
    # plt.plot(t_rain, df["t_air"], linewidth=1,linestyle='-',color='r', label='QAS_L')
    
    df.index = pd.to_datetime(df.time)
    fig, ax = plt.subplots(figsize=(14,10))
    plt.close()
    plt.plot(df["air_temperature_C"])
    plt.title(file)
    
    if i==0:
        header = ["time_UTC","air_temperature_C","precip_mm_uncorrected"]
        df0=df[header]
    else:
        header = ["time_UTC","air_temperature_C","precip_mm_uncorrected"]
        df1=df[header]
#%% write out

import matplotlib.dates as mdates

dfx = pd.concat([df0, df1], ignore_index=False, sort=False)
# plt.plot(dfx["air_temperature_C"])
#%%
plt.close()
fig, ax = plt.subplots(figsize=(14,10))
dfx.index = pd.to_datetime(dfx.time_UTC)

ax.plot(dfx["precip_mm_uncorrected"],label='precipitation')


fs=16
ax.tick_params(axis='both', which='major', labelsize=fs)
ax.tick_params(axis='both', which='minor', labelsize=fs)
# ax.set_ylabel(units+' anomaly relative to '+str(clim_lut.minyear[0])+' to 2022',fontsize=fs)
# lonx=-lon
# print(" %.4f" % lat+", %.4f" % lonx+", "+" %.0f" % elev)
# ax.set_title(current_year+' '+varname+' at '+site+" %.3f" % lat+"°N %.3f" % lonx+"°W "+" %.0f" % elev+" m",fontsize=fs*1.1)
ax.legend(prop={'size': fs*0.8})
ax.set_ylabel('mm',fontsize=fs)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y %b %d'))
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center',fontsize=fs)

plt.show()

#%%
# vals=['air_temperature_C','precip_mm_uncorrected']
# for val in vals:
#     dfx[val] = dfx[val].map(lambda x: '%.1f' % x) 
    
# dfx.to_csv('./precipitation_temperature_gauge/'+site+'_2020_to_2022'+'.csv',index=None)
