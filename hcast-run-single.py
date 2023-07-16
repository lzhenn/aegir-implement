#/usr/bin/env python3
'''
Date: Jun 20, 2022 

This is the top driver for aegir hindcast simulation 

Revision:
Nov 13, 2021 --- Fit for Njord Pipeline
Jun 21, 2022 --- Fit for Aegir Pipeline
Jul 14, 2023 --- Modify for Aegir Operational

Zhenning LI
'''
import os, sys
import datetime
import lib
from utils import utils

CWD=sys.path[0]

def main_run():
    
    # controller config handler
    cfg_hdl=lib.cfgparser.read_cfg(CWD+'/conf/config.hcast.ini')

 
    init_ts=datetime.datetime.strptime(
            cfg_hdl['AEGIR']['model_init_ts'], '%Y%m%d%H')
    run_days=int(cfg_hdl['AEGIR']['model_run_days'])
    roms_domain_root=CWD+'/domaindb/'+cfg_hdl['AEGIR']['nml_temp']+'/'
   
    if cfg_hdl['AEGIR']['case_name'] == '@date':
        cfg_hdl['AEGIR']['case_name']=cfg_hdl['AEGIR']['model_init_ts']
        
    # -----------ROMS DOWNLOAD AND INTERP-----------
    if cfg_hdl['ROMS']['download_flag']=='1':
        argline=utils.form_args(
            # 1
            init_ts.strftime('%Y%m%d%H'),
            # 2
            utils.parse_fmt_timepath(init_ts,cfg_hdl['ROMS']['raw_root']),
            # 3, # 4
            str(run_days),cfg_hdl['AEGIR']['nml_temp']
        )
        if cfg_hdl['ROMS']['raw_fmt']=='hycom': 
            ecode=os.system(
                'python3 '+CWD+'/pre_driver/roms_drv/down-hycom-analysis.py '+argline)        
        elif cfg_hdl['ROMS']['raw_fmt']=='cfs': 
            ecode=os.system(
                'sh '+CWD+'/pre_driver/roms_drv/cfsv2ocn_operational_collector.sh '+argline)        
        if ecode>0:
            utils.throw_error('Error in preparing ROMS icbc file!')
    
    if cfg_hdl['ROMS']['interp_flag']=='1':
        # build icbc maker 
        ecode=os.system('python3 '+CWD+'/prep_roms_icbc.py')        
        if ecode>0:
            utils.throw_error('Error in preparing ROMS icbc file!') 
    
    # ----------------WRF PREPROCESS---------------
    if cfg_hdl['WRF'].getboolean('run_wrf_driver'):
        cfg_smp=lib.cfgparser.read_cfg(CWD+'/wrf-top-driver/conf/config.s2s.cfs.ini')
        
        # merge ctrler
        cfg_tgt=lib.cfgparser.merge_cfg(cfg_hdl, cfg_smp)

        # write ctrler
        lib.cfgparser.write_cfg(cfg_tgt, CWD+'/wrf-top-driver/conf/config.ini')
        
        # run wrf-top-driver
        os.system('cd wrf-top-driver; python serial_driver.py')
    # ------------------AEGIR LOOP-------------------
    curr_ts=init_ts
    continue_flag=cfg_hdl['AEGIR'].getboolean('continue_run')
    # use resubmit tech for long runs to avoid large file/stability issues
    for iday in range(run_days):
        # 1
        args=cfg_hdl['WRF']['wrf_root']+' '
        # 2
        args=args+curr_ts.strftime('%Y-%m-%d_%H')+' '
        # 3 init run flag
        if (iday==0 and not(continue_flag)):
            args=args+'1'+' ' # init run
        else:
            args=args+'0'+' '
        # 4
        args=args+cfg_hdl['AEGIR']['case_name']+' '
        # 5
        args=args+cfg_hdl['AEGIR']['nml_temp']+' '
        # 6 AEGIR_ROOT
        args=args+CWD+'/Aegir/'+' '
        # 7 RA_ROOT
        args=args+cfg_hdl['ROMS']['ra_root']+' '
        # 8 ARCH_ROOT
        args=args+cfg_hdl['AEGIR']['arch_root']+' '
        # 9 ROMS DT
        args=args+cfg_hdl['ROMS']['dt']+' '
        # 10 WRF RST
        if (iday==0):
            args=args+cfg_hdl['WRF']['restart_run']+' '
        else:
            args=args+'1'+' '
        # 11 OFFSET_DAY
        #args=args+str(iday)+' '
        args=args+'1 '
    
        # run hcast-ctl.sh
        os.system('sh '+CWD+'/hcast-ctl.sh '+args)
        curr_ts=init_ts+datetime.timedelta(days=iday+1)

if __name__ == '__main__':
    main_run()
