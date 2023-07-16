# AEGIR Implement

Control script pipeline for WRF-ROMS (Aegir) coupled run. This pipeline may be seperated into `preprocessing` and `implementing` sections. 
`preprocessing` scetion aims at preprocessing driving data (e.g. CFS/HYCOM/ERA5) into initial and boundary conditions for ROMS and WRF.
`implementing` section controls the WRF+ROMS main model simulation stream.

## Setup

1. Create new conda environment and install required packages:
```
conda create -n aegir python=3.10
conda activate aegir
conda install xarray scipy 
conda install -c conda-forge eccodes
pip3 install eccodes cfgrib
```
2. modify `AEGIR_ROOT` and `DOMDB_PATH` in `setup.py`. 
`AEGIR_ROOT` points to the directory where the executable `coawstM` exists. `DOMDB_PATH` points to ROMS domain/sample files.
run `setup.py` to link domaindb folder to this working directory.
```bash
python3 setup.py
```

## Implement
Edit `conf/config.hcast.ini` first, then run 
```bash
python3 hcast-run-single.py
```

## Debug Log
- May 15, 2022: SCRIP: Using single process version. 
- June 24, 2022: Using `xarray` to_netcdf with 'a' opt if the same obj used for 2 files will cause unexpected var value.
- June 25, 2022: ROMS: Restart default output time is 12Z

## Scratch
Install eccodes by:
```bash
 conda install -c conda-forge eccodes
 pip3 install eccodes
 pip3 install cfgrib
```

Zhenning LI
July 14, 2023
