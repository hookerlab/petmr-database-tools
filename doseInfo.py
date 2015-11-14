import pandas as pd
import json
import os

__author__ = 'jphan'

pathname = input('Enter Path to files')
pathList = []
for dirName, subdirList, fileList in os.walk(pathname):
    for fname in fileList:
        if 'Dose_info' in fname:
            pathList.append(os.path.join(dirName, fname))
print(pathList)

for file in pathList:
    # reads in excel file path from list
    data = pd.read_excel(file)
    print(list(data))

    # gets the number of rows
    num_rows = len(data)

    # fills in empty cells or variations of n/a with 'NULL'
    data.fillna(value='NULL', inplace=True)
    temp = 0
    nalist = ['n/a', 'N/A', 'N/a', 'n/A']
    while temp < num_rows:
        for col in data.ix[:, 0:16]:
            for y in nalist:
                if y == data[col][temp]:
                    data.ix[temp, col] = 'NULL'
                    break
        temp += 1





# saves modified data to csv file
writefile = pd.DataFrame(data)
writefile.to_csv('Dost_Info_mod.csv', index=False, na_rep='NULL')
    
