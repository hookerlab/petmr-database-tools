import pandas as pd
import json
import os

__author__ = 'jphan'

pathname = input('Enter Path to files')
pathList = []
for dirName, subdirList, fileList in os.walk(pathname):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        if 'Dose_info' in fname:
            pathList.append(os.path.join(dirName, fname))
            print('\t%s' % fname)
print(pathList)

for file in pathList:
    # reads in excel file path from list
    data = pd.read_excel(file)
    print(list(data))
    
    
