#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- version: python2.7 -*-

import numpy as np

import pygrib


# == define the global vars


def del_space(lst):
    while '' in lst:
        lst.remove('')
    return lst


def main():
    # 1. read data from MICAPS diamond-4 file
    with open('./16112008.000', 'r') as fin:
        all_the_context = fin.readlines()
    # print len(all_the_context)

    # 2. get data informations(observate date, begin lon(lat), end laon(lat) and so on)
    dataInfo = all_the_context[1].strip().split(' ')
    dataInfo = del_space(dataInfo)
    rows, cols = int(dataInfo[12]), int(dataInfo[13])
    SLAT, ELAT = float(dataInfo[10]), float(dataInfo[11])
    SLON, ELON = float(dataInfo[8]), float(dataInfo[9])

    # 3. get the observate data and adjusted its rows and cols
    thedata = []
    for _ in range(2, len(all_the_context)):
        theline = all_the_context[_].strip().split(' ')
        theline = del_space(theline)
        thedata.append(theline)

    Indata = np.array(thedata, dtype='float').reshape(rows, cols)
    print "observate data: ", Indata

    # 4. add metadata for grib2 format output data

    # #Indata.save(cubes[0],'output.grib2')


if __name__ == '__main__':
    main()
