#/usr/bin/env python
"""Commonly used utilities

    Function    
    ---------------
   
    throw_error(source, msg):
        Throw error with call source and error message

"""
#import numpy as np
#import pandas as pd
#import netCDF4 as nc4

import logging, logging.config

def throw_error(msg):
    '''
    throw error and exit
    '''
    logging.error(msg)
    exit(1)

def write_log(msg, lvl=20):
    '''
    write logging log to log file
    level code:
        CRITICAL    50
        ERROR   40
        WARNING 30
        INFO    20
        DEBUG   10
        NOTSET  0
    '''

    logging.log(lvl, msg)

def parse_fmt_timepath(tgt_time, fmtpath):
    '''
    parse time string to datetime object
    '''
    seg_path=fmtpath.split('@')
    parsed_path=''
    for seg in seg_path:
        if seg.startswith('%'):
            parsed_path+=tgt_time.strftime(seg)
        else:
            parsed_path+=seg
    return parsed_path

def form_args(*args):
    '''form arglines in commandline format'''
    return ' '.join(args)