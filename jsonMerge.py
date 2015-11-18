import pandas as pd
import json
from collections import OrderedDict

__author__ = 'jphan'

#get path to both JSON files
inp_rp = input('Enter path to RadioPharmLog.json: ')
inp_rp = inp_rp.strip()
inp_dose = input('Enter path to Dose_info.json: ')
inp_dose = inp_dose.strip()
data_rp = json.load(open(inp_rp), object_pairs_hook=OrderedDict)
data_dose = json.load(open(inp_dose), object_pairs_hook=OrderedDict)

#number of rows in each file
num_rowsRp = len(data_rp)
num_rowsDose = len(data_dose)



