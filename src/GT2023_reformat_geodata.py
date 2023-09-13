#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 6 Sept 2023

reformat Greenland Trees geodata

@author: jason box
"""

import pandas as pd
import os
import numpy as np
import simplekml
import gpxpy
from datetime import date, timedelta

# ## change to your system's login name to change dir for local work
if os.getlogin() == 'jason':
    base_path = '/Users/jason/Dropbox/Greenland Trees/GT_Geodata/GreenlandTrees/'
os.chdir(base_path)

def datesx(date0,date1):
    # difference between current and previous date
    delta = timedelta(days=1)
    # store the dates between two dates in a list
    dates = []
    while date0 <= date1:
        # add current date to list by converting  it to iso format
        dates.append(date0.isoformat())
        # increment start date by timedelta
        date0 += delta
    print('Dates between', date0, 'and', date1)
    print(dates)
    return dates

def outputx(sentence_list,year):
    sentence_list=np.array(sentence_list)
        
    # datex,namex,waypoint.latitude,waypoint.longitude,elev
    out=pd.DataFrame({
        'date':sentence_list[:,0].astype(str),
        # 'species':sentence_list[:,1],
        # 'height':sentence_list[:,2].astype(float),
        'name':sentence_list[:,1],
        'lat':sentence_list[:,2].astype(float),
        'lon':sentence_list[:,3].astype(float),
        'elev':sentence_list[:,4].astype(float),
        'location':sentence_list[:,5].astype(str),
        'location2':sentence_list[:,6].astype(str),
        'species':sentence_list[:,7].astype(str),
        'height':sentence_list[:,8].astype(float),
        'notes':sentence_list[:,9].astype(str),
        'persons':sentence_list[:,10].astype(str),
        'orig_name':sentence_list[:,11].astype(str),
        # 'notes':sentence_list[:,7].astype(str),
                      })

    out.elev[out.elev<1]=np.nan
    
    # format float
    vals=['lat','lon']
    for val in vals:
        out[val] = out[val].map(lambda x: '%.6f' % x)
    
    # format elev
    vals=['elev']
    for val in vals:
        out[val] = out[val].map(lambda x: '%.0f' % x)
    
    # out.notes[out.notes=='nan']=np.nan
    # out.species[out.species=='nan']=np.nan
    # out[out.species=='']=np.nan #!!
    out.elev[out.elev=='nan']=np.nan
    
    out=out.sort_values('date')
    out.reset_index(drop=True, inplace=True)

    # out['species'].replace('', np.nan, inplace=True)
    # out.dropna(subset=['species'], inplace=True)
    # print(out)
    
    # out.to_excel('./geodata/'+year+'_Qanassiasat_GreenlandTrees.xlsx')
    out.to_csv('./geodata/'+year+'_GreenlandTrees.csv')
    
#---------------- Tasiusaq info

df=pd.read_csv('./geodata/2023_Tasiusaq_notes.csv')
print(df.columns)
df_namex=df.number.astype(str).values
df_namexx=[]
for nam in df_namex:
    nam=nam.zfill(3)
    # print(nam)
    df_namexx.append(nam)
# len(df)
df_namex=np.array(df_namexx)

# ---------------------------------------------------------------------- 2023 etc
year='2023'

# df=pd.read_csv('/Users/jason/Dropbox/GT_Geodata/GT2022/GT TT DT trees planted - heights_2022.csv')
# print(df.columns)
# df_namex=df.number.astype(str).values
# df_namexx=[]
# for nam in df_namex:
#     nam=nam.zfill(3)
#     # print(nam)
#     df_namexx.append(nam)
# # len(df)
# df_namex=np.array(df_namexx)

# Load gpx.
gpx_path = '/Users/jason/Dropbox/Greenland Trees/GT_Geodata/GT2023/all_wpts_v3.GPX'
with open(gpx_path) as f:
    gpx = gpxpy.parse(f)

sentence_list=[]

# len(gpx.waypoints)

cc=0

for i,waypoint in enumerate(gpx.waypoints):
    location=''
    elev=waypoint.elevation
    datex=pd.to_datetime(waypoint.time)#.strftime('%Y/%b/%d')
    # print(waypoint)
    # print(i,datex)
    yearx=datex.strftime('%Y')

    namex=waypoint.name
    orig_name=namex
    
    if namex=='Tas 20230001':namex='Forloh 1'
    if namex=='Tas 20230002':namex='Forloh 1'
    if namex=='Tas 20230003':namex='Forloh 1'
    if namex=='Tas 20230004':namex='Forloh 1'
    if namex=='Tas 20230005':namex='Forloh 1'
    if namex=='Tas 20230006':namex='Forloh 1'

    if ((yearx=='2023') & (waypoint.latitude<62)
        & (namex!='Forloh 1') & (namex!='Forloh 11')& (namex!='expediciones@inreach.gar')
        & (namex!='Ramon Laramendi basecamp by QAS_B nunatak') & (namex!='Nevada T') & (namex!='Hazard')
        & (namex!='Cam')
        &(namex[0:3] !='Uak')
        &(namex[0:8] !='Qan 2023')
        & (namex!='Nevada Larix 22')
        & (namex!='hotel0001')
        & (namex!='Nevada Poplus 22')
        & (namex!='Nevada pine23')
        & (namex!='Nevada larix 23')
        & (namex!='Tas 20230007')
        & (namex!='Tas 20230008')
        & (namex!='Tas 20230022')
        & (namex!='Tas 20230027')
        & (namex!='Behind hotel0001')
        & (namex!='Tiny forest 2023 new0016')
        & (namex!='Tiny forest 2023 new0017')
        & (namex!='11 2020? Larix')
        ):
        
        species='' ;notes='';location2=''; persons=''

        height=np.nan

        namex=namex.replace('Hotel2300','contorta ')
        namex=namex.replace('Narsaq PCohen0001','Narsaq PC')
        namex=namex.replace('Narsaq PC','poplus 2022 PC')
        namex=namex.replace('Sitca00','sylvestrus 20220829 ')
        namex=namex.replace('Tiny forest 2023 new00','TF 2023 ')
        namex=namex.replace('Sylvest 00','sylvestrus 20220905 ')
        namex=namex.replace('Pinus UAK00','sylvestrus 20220903 ')
        
        print(datex,orig_name)

        if namex[0:11] !='poplus 2022':
        # if namex[0:3] =='Tas':
        # if namex !='null':
        
    
            cc+=1
            
            v=np.where(df_namex==namex)
            # print(v[0][0])
            # print(i,namex)
            print(i,v,len(v))
            v=np.array(v)
            if v.size>0:
                # if len(v)>0:
                v=v[0][0]
                height=df['height'].values[v]
                species=df['type'].values[v]
                notes=df['notes'].values[v]
                # print(namex,height,source)

            if namex=='TF 2023 01':
                species='engelmannii'
                height=19.5
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 02':
                species='larix'
                height=15
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 03':
                species='contorta'
                height=37
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 04':
                species='engelmannii'
                height=26
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 05':
                species='larix'
                height=13
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 06':
                species='larix'
                height=18
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 07':
                species='larix'
                height=18
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 08':
                species='larix'
                height=6
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 09':
                species='engelmannii'
                height=13
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 10':
                species='larix'
                height=18
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 11':
                species='larix'
                height=15
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 12':
                species='larix'
                height=23
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 13':
                species='larix'
                height=13
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 14':
                species='contorta'
                height=31.5
                notes='bent stem'
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex=='TF 2023 15':
                species='larix'
                height=25
                elev=15 ; location2='Tiny_Forest'; notes='NE corner'
            if namex[0:6]=='poplar':
                # namex='Tas boulders and tires'
                species='poplus'
                height=30
                elev=15
                datex=pd.to_datetime('2023-05-24 12:07:00+00:00	')
                location='Narsaq'
                location2='Tiny_Forest'
                persons='Faezeh, Dirk'
                notes='cuttings from Narsarsuaq spring 2022'
            if namex=='Tas 18 boulders and tires':
                namex='Tas boulders and tires'
                species='engelmannii'
                height=7
                elev=15
                datex=pd.to_datetime('2023-08-24 17:07:00+00:00	')
            if namex=='Tas 19 boulders and tires':
                namex='Tas boulders and tires'
                species='larix'
                height=30
                elev=15
                datex=pd.to_datetime('2023-08-24 17:08:00+00:00	')#.strftime('%Y/%b/%d')
            if namex[0:8]=='contorta':
                species='contorta'
            if namex[0:6]=='Engelm':
                species='engelmannii'
            if namex[0:5]=='Alder':
                species='alnus'
            if namex[0:10]=='sylvestrus':
                species='sylvestrus'
            if namex=='0077':species='alnus'
            if namex=='0078':species='alnus'
            if namex=='0079':species='alnus'
            if namex=='0080':species='alnus'
            if namex=='0081':species='alnus'
            if namex=='0082':species='alnus'
            if namex=='0083':species='alnus'
            if namex=='0084':species='alnus'
            if namex=='0085':species='alnus'
            if namex=='0086':species='alnus'
            if namex=='0087':species='alnus'
            if namex=='0088':species='alnus'
            if namex=='0089':species='alnus'
            if namex=='0090':species='alnus'
            if namex=='0091':species='alnus'
            if namex=='0092':species='alnus'
            if namex=='0093':species='alnus'
            if namex=='0094':species='alnus'
            if namex=='0095':species='alnus'
            if pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-08-19':
                location='Narsaq'
                location2='Tiny_Forest'
                persons='Jason, Mette, Anna, Reinder'
            if pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-08-21':
                location='Narsaq'
                persons='Jason, Paul'
            if pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-08-24':
                location='Tasiusaq'
                location2='Tasiusaq'
                persons='Jason, Jacob, Mette'
            if pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-08-25':
                location='Tasiusaq'
                location2='Tasiusaq'
                persons='Jason, Jacob, Mette'
            if pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-08-28':
                location='Narsarsuaq'
                location2='hotel'
                persons='Jason, Jacob, Mette'
            if pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-08-29':
                location='Narsarsuaq'
                persons='Jason, Jacob, Mette, Filip'
            if ((pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-08-29')
                &(species=='alnus')):
                location2='IKEA'
                persons='Jason, Jacob, Mette, Filip'
            if ((pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-08-29')
                &(species=='sylvestrus')):
                location2='hospital_valley'
                persons='Jason, Jacob, Mette, Filip'
            if pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-09-03':
                location='Narsarsuaq'
            if ((pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-09-03')
                &(species=='sylvestrus')):
                location2='IKEA'
                persons='Jason, Jacob'
            if ((pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-09-03')
                &(species=='alnus')):
                location2='IKEA'
                persons='Jason, Jacob'
            if pd.to_datetime(datex).strftime('%Y-%m-%d')=='2023-09-05':
                location='Narsarsuaq'
                location2='hotel'
                persons='Jason, Jacob, Ray, Mark'

            # print(cc,datex,yearx,namex,waypoint.latitude,waypoint.longitude)
            sentence=datex,namex,waypoint.latitude,waypoint.longitude,elev,location,location2,species,height,notes,persons,orig_name
    # sentence=datex,species,height,source,lat,lon,elev

            # print(sentence)
            sentence_list.append(sentence)
            
            do_kml=1
            if do_kml:
                kml = simplekml.Kml(open=1)
                pnt = kml.newpoint(name='')
                pnt.coords=[(waypoint.longitude,waypoint.latitude)]
                # pnt.style.labelstyle.color = simplekml.Color.red  # Make the text red
                pnt.style.labelstyle.scale = 1.  # text scaling multiplier
                pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
                pnt.style.iconstyle.scale = 0.6  # Icon thrice as big
                pnt.altitudemode = simplekml.AltitudeMode.clamptoground
                
                opath='./geodata/kml/'+location2+'/'
                os.system('mkdir -p '+opath)
                kml_ofile=opath+datex.strftime('%Y%m%d')+' '+namex+".kml"
                kml.save(kml_ofile)

outputx(sentence_list,year)

#%%

df=pd.read_csv('./geodata/2023_GreenlandTrees.csv')

dates=datesx(date(2023, 5, 18),date(2023, 9, 5))

species=['engelmannii','larix','contorta','sylvestrus','alnus','poplus']
cc=0
for datex in dates:
    v=np.where(pd.to_datetime(df.date.values).strftime('%Y-%m-%d')==datex)
    cc+=len(v[0])
    if len(v[0])>0:
        print()

        print(datex,len(v[0]),cc)
    for speciesx in species:
        v=np.where((pd.to_datetime(df.date.values).strftime('%Y-%m-%d')==datex)
                   &(df.species==speciesx))
        if len(v[0])>0:
            print(speciesx,len(v[0]))
    
#%%
for speciesx in species:
    v=np.where(df.species==speciesx)
    if len(v[0])>0:
        print(speciesx,len(v[0]))