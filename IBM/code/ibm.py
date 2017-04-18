#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os

import numpy as np
import pandas as pd

import gribapi
import iris
import iris_grib
from iris.coords import DimCoord
from iris.cube import Cube

inDir = "./sj/mm/"

files = os.listdir(inDir)
for ff in files:
    # name, fh = ff[0:8], ff[9:13]
    # print fh
    df = pd.read_table(inDir + ff, skiprows=4,
                       header=None, delim_whitespace=True)
    data = df.as_matrix(columns=None).ravel()
    data = [_ for _ in data if not np.isnan(_)]
    data = [_ if _ != 9999.00 else np.nan for _ in data]
    data = np.array(data)
    data = np.reshape(data, (35, 37))

    latitude = DimCoord(np.linspace(29.45, 20.70, 35),
                        standard_name='latitude', units='degrees')
    longitude = DimCoord(np.linspace(97.33, 106.58, 37),
                         standard_name='longitude', units='degrees')
    time = DimCoord(0, standard_name='time', units='hours since {}'.format(
        str(datetime.datetime(2017, 3, 2, 17))))
    forecast_period = DimCoord(
        int(000), standard_name='forecast_period', units='hours')

    cube = Cube(data, dim_coords_and_dims=[(latitude, 0), (longitude, 1)], units='m s-1',
                standard_name='wind_speed')

    cube.add_aux_coord(time)
    cube.add_aux_coord(forecast_period)
    cube.coord(axis='X').coord_system = iris.coord_systems.GeogCS(654321)
    cube.coord(axis='Y').coord_system = iris.coord_systems.GeogCS(654321)

    # iris_grib.save_grib2(cube, "%s%s_EC-1000hpa-24h_temperature-CHINA_0.25deg.grib2" %(name, fh), append=False)
    iris_grib.save_grib2(
        cube, "2017030217%s%s_MICAPS_wind-speed_YUNNAN_27km.grib2" % (name, fh), append=False)
# print cube.data
