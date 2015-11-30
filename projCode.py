""" projCode.py

    Usage:
        projCode.py
        projCode.py [<Merged_File_Path>]

    Options:
        Merged_File_Path  : Path to merged.json
"""
from docopt import docopt
import pandas as pd
import json
from collections import OrderedDict
import os
import subprocess

__author__ = 'jphan'
'''
Merges RadioPharmLog.json and Dose_info.json
Outputs:
-Merged JSON files
-Modified JSON dose_info_with_ID
'''

#  C:/Users/strike/Desktop/projFiles2/merged.json
inp_merge = ''
if __name__ == "__main__":
    args = docopt(__doc__)
    boo = False
    if args["<Merged_File_Path>"]:
        inp_merge = str(args["<Merged_File_Path>"])
        inp_merge = inp_merge.strip()
        boo = True

    elif boo == False:
        #get path to both JSON files
        inp_merge = input('Enter path to merged.json: ')
        inp_merge = inp_merge.strip()

    #reads in json files
    data = pd.read_json(inp_merge, convert_dates=False)

    #number of rows
    num_rows = len(data)

    print(list(data))

    #creates new column
    data['project_code'] = 'NULL'

    #loop through each row in ID to find project code


    #creates dictionary to save as JSON object - Merged JSON
    rpList = []
    count = 0
    while count < num_rows:
        rp = OrderedDict()
        for col in data:
            rp[col] = data[col][count]
        rpList.append(rp)
        count += 1

    print(rpList)
    # j = json.dumps(rpList)
    # # print(j)
    # savePath = input('Enter save directory path for project_code JSON: ')
    # savePath = savePath.strip()
    # completeName = os.path.join(savePath, 'project_code.json')
    # print('Saving: ' + completeName)
    # with open(completeName, 'w') as f:
    #     f.write(j)
