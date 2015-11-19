import pandas as pd
import json
from collections import OrderedDict
import sys
import os

__author__ = 'jphan'
'''
Merges RadioPharmLog.json and Dose_info.json
Outputs:
-Merged JSON files
-Modified JSON dose_info_with_ID
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
    inp_rp = inp_rp.strip()
    inp_dose = input('Enter path to Dose_info.json: ')
    inp_dose = inp_dose.strip()

#reads in json files
data_rp = pd.read_json(inp_rp, convert_dates=False)
data_dose = pd.read_json(inp_dose)

#number of rows in each file
num_rowsRp = len(data_rp)
num_rowsDose = len(data_dose)

#converts Dose_info columns to object to allow serializability
for col in data_dose:
    data_dose[col] = data_dose[col].astype(object)

#Creates new 'NULL' columns in radiopharm dataframe with column names of dose_info columns
for col in data_dose:
    data_rp[col] = 'NULL'
#creates new column in dose_info for ID
data_dose['ID'] = 'NULL'
data_dose['Row Index'] = 'NULL'

def dateconv(date):
    """ converts date mm/dd/yyyy to yyyy-mm-dd
    Parameters:
    date: String
        String of date of the current row in the 'Date' column
    Returns:
    Out: String
        Returns reformatted date yyyy-mm-dd
    """
    formtype = ['%Y%m%d', '%Y-%m-%d']
    for f in formtype:
        try:
            dt = pd.datetime.strptime(str(data_dose['scan date(YYYYMMDD)'][date]), f).date()
            break
        except ValueError:
            pass
    return dt
    
#convert dose_info date to date format
row = 0
dose_dateList = []
while row < num_rowsDose:
    currDate = dateconv(row)
    dose_dateList.append(currDate)
    data_dose.ix[row, 'scan date(YYYYMMDD)'] = str(currDate)
    row += 1
    
def loopMerge(dose_row, start, end):
    """
    Parameters:
    dose_row: int
        Current row in dose_info.json file
    start: int
        Lower bound for range of current dose_info year
    end: int
        Upper bound for range of current dose_info year
    """
    while start <= end:
        if (str(data_dose['scan date(YYYYMMDD)'][dose_row]) == str(data_rp['Date'][start]) and
                data_dose['toi'][dose_row] == data_rp['Injection Time'][start]):
            data_dose.ix[dose_row, 'ID'] = data_rp['ID'][start]
            data_dose.ix[dose_row, 'Row Index'] = int(start) + 2
            for cols in data_dose:
                if cols != 'quant_param':
                    if cols != 'ID':
                        if cols != 'Row Index':
                            data_rp.ix[start, cols] = data_dose[cols][dose_row]
                else:
                    data_rp.set_value(start, cols, data_dose[cols][dose_row])
            break
        start += 1

'''
Year - Rows
2010 - 0-12
2011 - 13-55
2012 - 56-266
2013 - 267-575
2014 - 576-904
2015 - 905-(num_rowsRp-1)
'''
#Merge files based on Date and Time checks
row_dose = 0
while row_dose < num_rowsDose:
    if dose_dateList[row_dose].year == 2010:
        loopMerge(row_dose, 0, 12)
    elif dose_dateList[row_dose].year == 2011:
        loopMerge(row_dose, 13, 55)
    elif dose_dateList[row_dose].year == 2012:
        loopMerge(row_dose, 56, 266)
    elif dose_dateList[row_dose].year == 2013:
        loopMerge(row_dose, 267, 575)
    elif dose_dateList[row_dose].year == 2014:
        loopMerge(row_dose, 576, 904)
    elif dose_dateList[row_dose].year == 2015:
        loopMerge(row_dose, 905, 1173)
    else:
        loopMerge(row_dose, 1174, (num_rowsRp - 1))
    row_dose += 1
    
#creates dictionary to save as JSON object - Merged JSON
rpList = []
count = 0
while count < num_rowsRp:
    rp = OrderedDict()
    for col in data_rp:
        rp[col] = data_rp[col][count]
    rpList.append(rp)
    count += 1

j = json.dumps(rpList)
# print(j)
savePath = input('Enter save directory path for Merged JSON: ')
savePath = savePath.strip()
completeName = os.path.join(savePath, 'merged.json')
print('Saving: ' + completeName)
with open(completeName, 'w') as f:
    f.write(j)

#creates dictionary to save as JSON object - dose_info with ID + row index JSON
doseList = []
count = 0
while count < num_rowsDose:
    dose = OrderedDict()
    for col in data_dose:
        dose[col] = data_dose[col][count]
    doseList.append(dose)
    count += 1

k = json.dumps(doseList)
# print(k)
savePath = input('Enter save directory path for Dose_info with ID JSON: ')
savePath = savePath.strip()
completeName = os.path.join(savePath, 'Dose_info_with_ID.json')
print('Saving: ' + completeName)
with open(completeName, 'w') as f:
    f.write(k)
    
