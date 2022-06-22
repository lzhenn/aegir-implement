import sys
import xarray as xr
import numpy as np

aegir_path=sys.argv[1]
ymd=sys.argv[2]


HALF_DAY=43200000000000

# bdy no ocean_time
timevar_lst_bdy=['v2d','v3d','temp','salt', 'zeta']
# clm with ocean_time
timevar_lst_clm=['v2d','v3d','temp','salt', 'zeta', 'ocean']

bdy_file=aegir_path+'/ow_icbc/d01/coawst_bdy_'+ymd+'.nc'
clm_file=aegir_path+'/ow_icbc/d01/coawst_clm_'+ymd+'.nc'

d = xr.load_dataset(bdy_file)
for var in timevar_lst_bdy:
    var_time=d[var+'_time']

    var_time.values[:]=var_time.values[:]+HALF_DAY
    d=d.assign_coords({var:var_time})

d.to_netcdf(bdy_file,'a')

d = xr.load_dataset(clm_file)
for var in timevar_lst_bdy:
    var_time=d[var+'_time']

    var_time.values[:]=var_time.values[:]+HALF_DAY
    d=d.assign_coords({var:var_time})

d.to_netcdf(clm_file,'a')
