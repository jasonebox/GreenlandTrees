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

files=['QANASIASSAT_UTC_2020-2021','QANASIASSAT_UTC_2021-2022','QANASIASSAT_UTC_2022-2023']
# files=['QANASIASSAT_UTC_2020-2021']

iyear=2020 ; fyear=2023

n_years=len(files)
prate=np.zeros(n_years)

for i,file in enumerate(files):
    # if i==2:
    if i>=0:
        #------------------------------------------------------------------ rain data
        if site == 'QANASIASSAT':
            fn="./precipitation_temperature_gauge/raw/"+file+".csv"
            SN="20362477"
            epoch="20190830"
            timex="Date Time, GMT+00:00"
            if i==0:
                time_format='%m/%d/%y %I:%M:%S %p'
            if i==1:
                time_format='%m/%d/%Y %I.%M.%S %p'
            if i==2:
                time_format='%m/%d/%y %I:%M:%S %p'
    
            
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
        
        df["accumulated_precipitation"]=df["event"] * 0.2
        
        # year_rain=t_rain.dt.year
        # month_rain=t_rain.dt.month
        # day_rain=t_rain.dt.day
        # hour_rain=t_rain.dt.hour
        # min_rain=t_rain.dt.minute
        
        # #print(hour_rain)
        
        # n_rows_rain_data = len(ppt)
        prate[i]=np.nanmax(df["accumulated_precipitation"])
        
        ppt_offset=0
        if i==0:
            df["air_temperature_C"]= (df.T2m - 32) * 5/9.
            ppt_offset=np.nanmax(df["accumulated_precipitation"])
        else:
            df["air_temperature_C"]=df.T2m
            df["accumulated_precipitation"]+=ppt_offset
        
        df.index = pd.to_datetime(df.time)

        ##%% plot data
        do_plot=0
        if do_plot:
            from datetime import datetime
            import matplotlib.dates as mdates
    
            fs=22
    
            t0=datetime(2022, 9, 1) ; t1=datetime(2022, 9, 30)
            # plt.plot(t_rain, ppt, linewidth=1,linestyle='-',color='r', label='QAS_L')
            # plt.plot(t_rain, df["t_air"], linewidth=1,linestyle='-',color='r', label='QAS_L')
            
            fig, ax = plt.subplots(figsize=(14,10))
            # plt.close()
            # plt.clf()
            plt.plot(df["air_temperature_C"][t0:t1],'.')
            df.columns
            ax.set_title(file,fontsize=fs)
            
            # ax.set_xlim(t0,t1)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center',fontsize=fs)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
            # ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
            ax.tick_params(axis='both', which='major', labelsize=fs)
            ax.tick_params(axis='both', which='minor', labelsize=fs)
    
            plt.show()
##% concat
        if i==0:
            header = ["time_UTC","air_temperature_C","accumulated_precipitation"]
            df0=df[header]
        if i==1:
            header = ["time_UTC","air_temperature_C","accumulated_precipitation"]
            df1=df[header]
        if i==2:
            header = ["time_UTC","air_temperature_C","accumulated_precipitation"]
            df2=df[header] 
            
    print('annual precipitation',prate)
#%% write out

import matplotlib.dates as mdates

dfx = pd.concat([df0, df1,df2], ignore_index=False, sort=False)
# plt.plot(dfx["air_temperature_C"])
#%%
plt.close()
fig, ax = plt.subplots(figsize=(14,10))
dfx.index = pd.to_datetime(dfx.time_UTC)

ax.plot(dfx["accumulated_precipitation"],label='accumulated precipitation')


fs=16
ax.tick_params(axis='both', which='major', labelsize=fs)
ax.tick_params(axis='both', which='minor', labelsize=fs)
# ax.set_ylabel(units+' anomaly relative to '+str(clim_lut.minyear[0])+' to 2022',fontsize=fs)
# lonx=-lon
# print(" %.4f" % lat+", %.4f" % lonx+", "+" %.0f" % elev)
ax.set_title(site)
ax.legend(prop={'size': fs*0.8})
ax.set_ylabel('mm',fontsize=fs)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y %b %d'))
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center',fontsize=fs)

plt.show()

#%%
vals=['air_temperature_C','accumulated_precipitation']
for val in vals:
    dfx[val] = dfx[val].map(lambda x: '%.1f' % x) 
    
dfx.to_csv('./precipitation_temperature_gauge/output/'+site+'_'+str(iyear)+'_to_'+str(fyear)+'_hourly_air_T_precip_events.csv',index=None)
# dfx.to_excel('./precipitation_temperature_gauge/'+site+'_2020_to_2022'+'.xlsx',index=None)
