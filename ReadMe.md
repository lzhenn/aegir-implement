# AEGIR Implement

Control script pipeline for WRF-ROMS (Aegir) coupled run.

## Setup
run `setup.py` to link domaindb folder to this working directory.

## Implement
Edit `conf/config.hcast.ini` first, then run 
```bash
python3 hcast-run-single.py
```

## Debug Log
May 15, 2022: SCRIP: Using single process version. 
June 24, 2022: Using `xarray` to_netcdf with 'a' opt if the same obj used for 2 files will cause unexpected var value.
June 25, 2022: ROMS: Restart default output time is 12Z

Zhenning LI
June 24, 2022
