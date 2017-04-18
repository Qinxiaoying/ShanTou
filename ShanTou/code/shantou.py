#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import unicode_literals

import os
import numpy as np
import pandas as pd
from datetime import datetime
from collections import OrderedDict
import get_airpollution_obs_hourly as gh


fnd = '/home/enso/Qxy/get_obs_air'
station_code = ['1001A', '1002A', '1003A', '1004A', '1005A', '1006A', '1007A']

ELE = OrderedDict()
ELE['100'] = 'so2'
ELE['101'] = 'no2'
ELE['103'] = 'co'
ELE['102'] = 'o3'
ELE['104'] = 'pm10'
ELE['105'] = 'pm25'


def read_all_data(YY, MM, DD):
    dd = pd.DataFrame(columns=['StationCode', 'TimePoint', 'PollutantCode', 'MonValue', 'Mark', 'DataStatus'])
    
    for i in range(24):
        for st_code in station_code:
            data = gh.get_airpollution_obs_hourly(station_code=st_code, time_point=datetime(YY, MM, DD, i))
            dd = pd.concat([dd, data])
            
    return dd.sort_values(by=['StationCode', 'TimePoint', 'PollutantCode'])


def cal_mean_6h(YY, MM, DD):
    dd = read_all_data(YY, MM, DD)
    stinfo = pd.read_csv(os.path.join(fnd, 'station.csv'), index_col=0)
    index = list(range(24))
                                   
    for i in range(0, 24, 6):
        data_all = []
        for st in station_code:
            data_6h = []
            st_lon = float(stinfo.Longitude[stinfo.StationCode == st])
            st_lat = float(stinfo.Latitude[stinfo.StationCode == st])
            data_6h.append(st)
            data_6h.append('{0:4}'.format(YY))
            data_6h.append('{0:2}'.format(MM))
            data_6h.append('{0:2}'.format(DD))
            data_6h.append('{0:12}'.format(round(st_lon, 4)))
            data_6h.append('{0:12}'.format(round(st_lat, 4)))
            for key, val in ELE.items():
                dn = dd[dd.PollutantCode == key]
                dn = dn[dn.StationCode == st]
                dn.MonValue[dn.DataStatus != 2.0] = np.nan
                dn.MonValue.interpolate(limit=24, limit_direction='both')
                dn.index = index
                dn_mean = dn.MonValue.loc[i:i+6].mean()
                dn_mean = round(dn_mean, 3) if val == 'co' else int(dn_mean*1000)
                data_6h.append('{0:12}'.format(dn_mean)) if val == 'co' else data_6h.append('{0:8}'.format(dn_mean))
            data_all.append(data_6h)
            
        data_all = [' '.join(j) for j in data_all]
        fd = pd.DataFrame(data_all)
        fh = '0{}'.format(i + 6) if (i + 6) < 10 else i + 6
        M = '0{}'.format(MM) if MM < 10 else MM
        D = '0{}'.format(DD) if DD < 10 else DD
        fn = '{}{}{}_{}h_daily_city_obs.txt'.format(tt.year, M, D, fh)
        fn = os.path.join(fnd, 'out', fn)
        fd.to_csv(fn, index=False, header=False, mode='w', sep='_')

if __name__ == '__main__':
    tt = datetime.now()
    yy, mm, dd = tt.year, tt.month, tt.day-1
    cal_mean_6h(yy, mm, dd)
