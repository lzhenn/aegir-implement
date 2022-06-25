AEGIR_ROOT=$1
RA_ROOT=$2
STRT_DATE_FULL=$3
DT=$4
CASE_NAME=$5
INIT_RUN_FLAG=$6
OFFSET_DAY=$7

FCST_DAYS=1
AEGIR_PROJ_PATH=${AEGIR_ROOT}/Projects/Aegir/
# Set up paras derivatives 
STRT_DATE=${STRT_DATE_FULL:0:10}
INIT_HR=${STRT_DATE_FULL:11:2}
END_DATE=`date -d "$STRT_DATE +$FCST_DAYS days" "+%Y-%m-%d"`

STRT_DATE_PACK=${STRT_DATE//-/} # YYYYMMDD style
END_DATE_PACK=${END_DATE//-/}

ROMS_DOMAIN_ROOT=${AEGIR_PROJ_PATH}/roms_swan_grid/
ICBC_ROOT=${RA_ROOT}/icbc/${CASE_NAME}/

CLMFILE=Projects/Aegir/ow_icbc/d01/coawst_clm_${STRT_DATE_PACK}.nc
BDYFILE=Projects/Aegir/ow_icbc/d01/coawst_bdy_${STRT_DATE_PACK}.nc


NTIMES=`expr $FCST_DAYS \* 86400 / $DT `

echo ">>>>ROMS: run roms_hcast_driver.sh..."

# modify roms.in
ROMS_IN=$AEGIR_PROJ_PATH/roms_d01.in
sed -i "s@NTIMES_placeholder@NTIMES == ${NTIMES}@" $ROMS_IN
sed -i "s@DT_placeholder@DT == ${DT}.0d0@" $ROMS_IN
sed -i "s@CLMNAME_placeholder@CLMNAME == ${CLMFILE}@" $ROMS_IN
sed -i "s@BRYNAME_placeholder@BRYNAME == ${BDYFILE}@" $ROMS_IN

# relink ROMS icbc
if [ $INIT_RUN_FLAG == 1 ]; then
    ICBC_LK=${AEGIR_PROJ_PATH}/ow_icbc/d01
    rm -f $ICBC_LK
    ln -sf ${ICBC_ROOT} ${ICBC_LK}
fi

# bug fix for bdy and clm files
python3 ./roms_drv/roms_bdy_clm_time_bug_patch.py $AEGIR_PROJ_PATH $STRT_DATE_PACK $INIT_RUN_FLAG $OFFSET_DAY
