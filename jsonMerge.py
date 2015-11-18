import pandas as pd
import json
from collections import OrderedDict
import sys

__author__ = 'jphan'
'''
Merges RadioPharmLog.json and Dose_info.json
Outputs:
-Merged JSON file
'''

'''
allows User to input arguments directly into cmd line
arg[1] must be RadioPharmLog.json path
arg[2] must be Dose_info.json path
'''
total = len(sys.argv)
if total == 3:
    inp_rp = str(sys.argv[1]).strip()
    inp_dose = str(sys.argv[2]).strip()

else:
    #get path to both JSON files
    inp_rp = input('Enter path to RadioPharmLog.json: ')
    # inp_rp = 'C:/Users/strike/Desktop/projFiles/RadioPharmLog.json'
    inp_rp = inp_rp.strip()
    inp_dose = input('Enter path to Dose_info.json: ')
    # inp_dose = 'C:/Users/strike/Desktop/projFiles/Dose_info.json'
    inp_dose = inp_dose.strip()

#reads in json files
data_rp = pd.read_json(inp_rp)
data_dose = pd.read_json(inp_dose)

#number of rows in each file
num_rowsRp = len(data_rp)
num_rowsDose = len(data_dose)



