#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aug 23 2023

@author: jason
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#plt.style.use('ggplot')
# from datetime import datetime

sites=['QANASIASSAT']


path='/Users/jason/Dropbox/Greenland Trees/GT_Geodata/GreenlandTrees/'

iyear=2020 ; fyear=2023

os.chdir(path)

for site in sites:

    x=1
    
    opath='/Users/jason/Dropbox/Greenland Trees/GT_Geodata/GreenlandTrees/precipitation_temperature_gauge/output/'
    
    fn='./precipitation_temperature_gauge/output/QANASIASSAT_2020_to_2023_hourly_air_T_precip_events.csv'
    # os.system('ls -lF '+fn )
    df = pd.read_csv(fn)
    
    month = pd.DatetimeIndex(df["time_UTC"]).month
    day = pd.DatetimeIndex(df["time_UTC"]).day
    year = pd.DatetimeIndex(df["time_UTC"]).year
    doy = pd.DatetimeIndex(df["time_UTC"]).dayofyear

    t=pd.to_datetime(df.time_UTC)
    year=t.dt.year
    
    df.columns

    ppt_rate_uncor_cum= df["accumulated_precipitation"]
    ppt_rate_uncor_cum[np.isnan(ppt_rate_uncor_cum)]=0
    df["precip_mm_uncorrected_event"]=0
    df["precip_mm_uncorrected_event"][df["accumulated_precipitation"]>0]=0.2
    df.index = pd.to_datetime(df.time_UTC)
        
    cc=0

    # ----------------------------- daily
    out_fn=opath+site+'_rain_data_daily_'+str(fyear)+'-'+str(fyear)+'.csv'
    out_f1=open(out_fn,'w')
    out_f1.write("year,month,day,day of year,date,tp\n")

    for y in range(iyear,fyear+1):
        for i in range(1, 366):
            v = np.where( (doy == i) & (year == y) )
            if len(v[0]) > 0:
                tot_uncor=sum(df["precip_mm_uncorrected_event"][v[0]])
                print(y,i,len(v[0]),tot_uncor)

                out_f1.write(str(y)+
                             ','+str(month[v[0][0]])+                             
                             ','+str(day[v[0][0]])+                             
                             ','+str(i)+
                             ','+str(pd.to_datetime(df.time_UTC[v[0][0]],format='%Y-%m-%d'))[0:10]+
                             ','+str("%.1f"%tot_uncor)+'\n')
                cc+=1
    out_f1.close()

    
#%% plot daily
print(site,cc)
df=pd.read_csv('/Users/jason/Dropbox/Greenland Trees/GT_Geodata/GreenlandTrees/precipitation_temperature_gauge/output/QANASIASSAT_rain_data_daily_2023-2023.csv')
df['date'] = pd.to_datetime(df[['year','month','day']])
df.columns

plt.plot(df['tp'])
plt.ylabel('mm per day')
#%%
# ----------------------------- monthly
out_fn=opath+site+'_rain_data_monthly_'+str(fyear)+'-'+str(fyear)+'.csv'
out_f1=open(out_fn,'w')
out_f1.write("year,month,tp\n")
    
for y in range(iyear,fyear+1):
    for i in range(1, 13):
        v = np.where( (df.month == i) & (df.year == y) )
        if len(v[0]) >= 28:
            tot_uncor=sum(df["tp"][v[0]])
            print(y,i,len(v[0]),tot_uncor)

            out_f1.write(str(y)+
                         ','+str(i)+
                             ','+str("%.1f"%tot_uncor)+'\n')
        else:
            out_f1.write(str(y)+
                         ','+str(i)+
                             ','+str("%.1f"%np.nan)+'\n')
out_f1.close()

#%% monthly barplot
do_plot=1
fs=20
if do_plot:
    from datetime import datetime
    import matplotlib.dates as mdates
    df=pd.read_csv(out_fn)
    print(df.columns)

    # df["time"]=pd.to_datetime(df['year'],df['month']) 
    # df["time"]=pd.to_datetime([df['year'],df['month']],format='%Y-%m')
    df["time"]=pd.to_datetime((df["year"]*100+df["month"]).apply(str),format='%Y%m')
    month = pd.DatetimeIndex(df["time"]).month
    year = pd.DatetimeIndex(df["time"]).year

    # df.index = pd.to_datetime(df.time)

    fig, ax = plt.subplots(figsize=(14,10))
    # plt.close()
    # plt.clf()
    # t0=datetime(2020, 9, 1) ; t1=datetime(2023, 9, 30)
    wid=0.2
    osx=0.1
    v=df.year==2020
    plt.bar(df["month"][v]-osx*2,df["tp"][v],width=wid,color='grey',label='2020')
    v=df.year==2021
    plt.bar(df["month"][v],df["tp"][v],width=wid,color='k',label='2021')
    v=df.year==2022
    plt.bar(df["month"][v]+osx*2,df["tp"][v],width=wid,color='b',label='2022')
    v=df.year==2023
    plt.bar(df["month"][v]+osx*4,df["tp"][v],width=wid,color='r',label='2023')

    plt.legend(fontsize=fs)
    df.columns
    ax.set_title('Qanassiasat monthly precip',fontsize=fs)
    ax.set_ylabel('mm',fontsize=fs)
    ax.set_xlabel('month',fontsize=fs)
    # ax.set_xlim(t0,t1)
    # plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center',fontsize=fs)
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y %b'))
    # ax.xaxis.set_major_locator(mdates.yLocator(interval=7))
    # ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
    ax.tick_params(axis='both', which='major', labelsize=fs)
    ax.tick_params(axis='both', which='minor', labelsize=fs)
    
    plt.show()
