#/usr/bin/env python3
'''
Date: Jan 31, 2022 

This is script will check the sanity of ROMS ICBC
and fix the absent file when necessary

Zhenning LI
'''
import os, sys
import datetime
import lib
import xarray as xr
import numpy as np

CWD=sys.path[0]

TIME_TAGS=['ocean', 'zeta', 'v2d', 'v3d', 'salt', 'temp']

def main_run():
    
    # controller config handler
    cfg_hdl=lib.cfgparser.read_cfg(CWD+'/conf/fcst.ini')
    
    if (cfg_hdl['INPUT']['model_init_ts']== 'realtime'):
        today = datetime.datetime.today()
        init_ts = today.replace(hour=12)
        cfg_hdl['INPUT']['model_init_ts']=init_ts.strftime('%Y%m%d%H')
    else:
        init_ts=datetime.datetime.strptime(
                cfg_hdl['INPUT']['model_init_ts'], '%Y%m%d%H')
       
    run_days=int(cfg_hdl['INPUT']['model_run_days'])
    icbc_dir=cfg_hdl['ROMS']['ra_root']+'/icbc/'+cfg_hdl['INPUT']['model_init_ts']+'/'
    
    if os.path.isfile(icbc_dir+'coawst_ini.nc'):
        print(icbc_dir+'coawst_ini.nc found.')
    else:
        print('No initial, exit!')
        exit()

    active_flag=True
    for iday in range(run_days):
        dis_sanity=0
        curr_ts=init_ts+datetime.timedelta(days=iday)
        clm_file=icbc_dir+'coawst_clm_'+curr_ts.strftime('%Y%m%d')+'.nc'
        bdy_file=icbc_dir+'coawst_bdy_'+curr_ts.strftime('%Y%m%d')+'.nc'
        if iday>0:
            ystd_ts=init_ts+datetime.timedelta(days=iday-1)
            if active_flag:
                clm_file_pr=icbc_dir+'coawst_clm_'+ystd_ts.strftime('%Y%m%d')+'.nc'
                bdy_file_pr=icbc_dir+'coawst_bdy_'+ystd_ts.strftime('%Y%m%d')+'.nc'

        if os.path.isfile(clm_file):
            print(clm_file+' found.')
        else:
            print(clm_file+' not found, try overwrite.')
            dis_sanity=dis_sanity+1
            active_flag=False
            #os.popen('cp '+clm_file_pr+' '+clm_file)
            d = xr.load_dataset(clm_file_pr)
            for tag in TIME_TAGS:
                time_tag=tag+'_time'
                d[time_tag].values[0]=d[time_tag].values[0]+np.timedelta64(dis_sanity,'D')
            d.to_netcdf(clm_file,'w')

        if os.path.isfile(bdy_file):
            print(bdy_file+' found.')
        else:
            print(bdy_file+' not found, try overwrite.')
            d = xr.load_dataset(bdy_file_pr)
            for tag in TIME_TAGS[1:]:
                time_tag=tag+'_time'
                d[time_tag].values[0]=d[time_tag].values[0]+np.timedelta64(dis_sanity,'D')
            d.to_netcdf(bdy_file,'w')
