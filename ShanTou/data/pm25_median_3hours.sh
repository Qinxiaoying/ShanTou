#!/bin/bash

# to get median values of so2, co, nox, o3, pm10, pm2.5 concentrations
# for every three hours

_YEAR=`date +%Y`
_DIRIN=/mnt/pm25/product/${_YEAR}convert
_DIROUT=/mnt/pm25/product/daily

if [ ! -d ${_DIROUT}/${_YEAR}/3hours ]; then
   mkdir -p ${_DIROUT}/${_YEAR}/3hours
fi

if [ -e ${_DIROUT}/input_3hours.txt ]; then
   cd ${_DIROUT}
   rm input_3hours.txt
fi

_DATECUR=`date  +%Y%m%d%H`

_HR=0
while [ $_HR -le 2 ]
do
  _DATE=`date -d "$_HR hours ago" +%Y%m%d%H`
  ls $_DIRIN/${_DATE}.txt >>${_DIROUT}/input_3hours.txt
  _HR=`expr $_HR + 1`
done

_TNL=`cat ${_DIROUT}/input_3hours.txt | wc -l`

if [ $_TNL -gt 0 ]; then
   ${_DIROUT}/precon.exe ${_DIROUT}/input_3hours.txt  ${_DIROUT}/output_3hours.txt
   mv  ${_DIROUT}/output_3hours.txt  ${_DIROUT}/${_YEAR}/3hours/${_DATECUR}_3hours_median.txt
elif [ $_TNL -gt 3 ]; then
     echo " The pm2.5 concentration observations in the date of ${_DATE} are wrong"
else
     echo " The pm2.5 concentration observations in the date of ${_DATE} are missing"
fi


