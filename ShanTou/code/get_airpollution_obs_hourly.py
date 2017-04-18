#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import logging
import pymssql
import numpy as np
import pandas as pd
from decimal import Decimal
from datetime import datetime, date, timedelta


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(BASE_DIR, 'get_airpollution_obs_hourly.log'),
    level=logging.INFO,
)


logger = logging.getLogger('get_airpollution_obs_hourly')


server = '172.16.178.98'
user = 'sa'
password = 'airauto'


station_info = pd.read_csv('EnvDataCity.dbo.Station.csv', index_col=0)
"""
  PositionName Area  UniqueCode StationCode   Longitude  Latitude
0         金平子站  汕头市   440500051       1001A  116.679400   23.3667
1         龙湖子站  汕头市   440500052       1002A  116.724400   23.3633
2         濠江子站  汕头市   440500054       1003A  116.725800   23.2775
3         澄海子站  汕头市   440500055       1004A  116.751900   23.4714
4         潮阳子站  汕头市   440500056       1005A  116.609200   23.2539
5         潮南子站  汕头市   440500057       1006A  116.401900   23.2536
6        南澳县子站  汕头市   440500058       1007A  117.023333   23.4200
"""

pollutant_info = pd.read_csv('EnvDataCity.dbo.Pollutant.csv')
pollutant_info.pop('PollutantId')
pollutant_info = pollutant_info[pollutant_info['PollutantCode']<=105]
"""
   PollutantCode PollutantName ChineseName   Unit  PollutantTypeId
0            100           SO2        二氧化硫  μg/m3                1
1            101           NO2        二氧化氮  μg/m3                1
2            102            O3          臭氧  μg/m3                1
3            103            CO        一氧化碳  mg/m3                1
4            104          PM10     颗粒物PM10  μg/m3                1
5            105         PM2.5   细颗粒物PM2.5  μg/m3                1
"""


def get_airpollution_obs_hourly(station_code='1001A', time_point=datetime(2017, 4, 10, 0)):
    """
    SELECT TOP 1000 [Id]
          ,[StationCode]
          ,[TimePoint]
          ,[PollutantCode]
          ,[MonValue]
          ,[Mark]
          ,[DataStatus]
      FROM [EnvDataCity].[dbo].[Air_h_2017_1007A_App]
    """
    conn = pymssql.connect(server, user, password, "EnvDataCity")
    cursor = conn.cursor()
    cursor.execute(
        'SELECT StationCode, TimePoint,PollutantCode,MonValue,Mark,DataStatus FROM dbo.Air_h_{}_{}_App WHERE TimePoint=%s AND PollutantCode<=105'.format(
            time_point.year, station_code),
        time_point.strftime('%Y-%m-%d %H:%M'))
    rows = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(rows, columns=['StationCode','TimePoint','PollutantCode','MonValue','Mark','DataStatus'])
    #print df
    return df


if __name__ == '__main__':
    get_airpollution_obs_hourly()
