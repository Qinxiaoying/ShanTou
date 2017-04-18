#!/bin/bash

# to calculate interpolated daily median values of so2, co, nox, o3, pm10, pm2.5 concentrations at
# data missing points
# for every three hours

 _DATE=`date +%Y%m%d%H`
 _YEAR=`date +%Y`

 echo $_DATE

 _DIRIN=/mnt/pm25/product/daily
 _DIRDATA=${_DIRIN}/${_YEAR}/3hours

 if [ ! -d ${_DIRDATA}/interpolate ]; then
    mkdir -p ${_DIRDATA}/interpolate 
 fi 

   _INFL=${_DIRDATA}/${_DATE}_3hours_median.txt
   _OFL=${_DIRDATA}/interpolate/${_DATE}_3hours_median.txt
 
   if [ -e $_INFL ]; then
     _TNL=`cat $_INFL | wc -l`
     $_DIRIN/interpolation.exe $_INFL $_TNL $_OFL
   else
     echo " The daily mean pm2.5 concentration observations in the date of ${_DATE} are missing" 
   fi


