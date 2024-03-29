#!/bin/sh
#------------------------------------------------------
# CFS collector is used to obtain operational CFSv2 
# 0d25 products.
#                                    Zhenning LI
#                                    Sep 6, 2021
#------------------------------------------------------

#------------------------------------------------------
# USAGE: 
# 
# If use from external call:
#   sh cfsv2_operational_collector.sh $INIT_YYYYMMDDHH $ARCH_PATH $FCST_DAYS
#   e.g. sh gfs_slicer.sh /home/metctm1/array/data 2021070512 1
#    
# Or you could remove the comment # from defined variables and
# assign them properly, just type: sh gfs_slicer.sh
#------------------------------------------------------

#https://www.ncei.noaa.gov/data/climate-forecast-system/access/operational-9-month-forecast/6-hourly-by-pressure/2021/202109/20210901/2021090100/pgbf2021090100.01.2021090100.grb2

# ------------Below for user-defined configurations ------------

# Initial time 
# 2021/202109/20210901/2021090100/
STRT_YMDH=$1
#STRT_YMDH=2022062700

# Archive path
ARCH_PATH=$2
#ARCH_PATH=/home/lzhenn/drv_field/cfs_ocn/$STRT_YMDH

if [ ! -d $ARCH_PATH ]; then
    mkdir $ARCH_PATH
fi

# How long period to fecth
FCST_DAY=$3
#FCST_DAY=40

# ------------Upper for user-defined configurations ------------
# The interval to fetch CFS output, 6-hr only

#  24-hr for CFS ocn data
FRQ=24

TOTAL_HR=`expr $FCST_DAY \* 24`

BASE_URL="https://www.ncei.noaa.gov/data/climate-forecast-system/access/operational-9-month-forecast/6-hourly-ocean/"
YYYY=${STRT_YMDH:0:4}
YYYYMM=${STRT_YMDH:0:6}
YYYYMMDD=${STRT_YMDH:0:8}
BASE_URL=$BASE_URL/${YYYY}/${YYYYMM}/${YYYYMMDD}/${STRT_YMDH}/

for CURR_HR in $(seq 24 $FRQ $TOTAL_HR) 
do
    
    CURR_TS=`date -d "${YYYYMMDD} ${STRT_YMDH:9:11} +${CURR_HR} hours" +%Y%m%d%H`
    FN_FILTER="ocnf"${CURR_TS}".01."${STRT_YMDH}".grb2"
      
    SRC_URL=${BASE_URL}${FN_FILTER} 
    wget ${SRC_URL} -O ${ARCH_PATH}/${FN_FILTER}

done 

DAY1_YMDH=`date -d "${YYYYMMDD} ${STRT_YMDH:9:11} +${FRQ} hours" +%Y%m%d%H`
DAY1_FILE="ocnf"${DAY1_YMDH}".01."${STRT_YMDH}".grb2"
DAY0_FILE="ocnf"${STRT_YMDH}".01."${STRT_YMDH}".grb2"

ln -sf  ${ARCH_PATH}/${DAY1_FILE} ${ARCH_PATH}/${DAY0_FILE}

