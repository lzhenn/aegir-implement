#!/usr/bin/env python3

import os
# set AEGIR_ROOT
AEGIR_ROOT='/home/metctm1/array_hq133/COAWST_Aegir'

# set DOMDB_PATH below to link the geo_em data
DOMDB_PATH='/home/lzhenn/array74/Njord_Calypso/domaindb'

os.system('ln -sf '+DOMDB_PATH+' ./domaindb')
os.system('ln -sf '+AEGIR_ROOT+' ./Aegir')
