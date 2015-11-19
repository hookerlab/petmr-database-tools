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
            # dt = pd.datetime.strptime(data['Date'][date], f)
            dt = pd.datetime.strptime(str(data_dose['scan date(YYYYMMDD)'][date]), f).date()
            break
        except ValueError:
            pass
    # return str('{0}-{1}-{2}'.format(dt.year, dt.month, dt.day % 100))
    return dt
    
#convert dose_info date to date format
row = 0
while row < num_rowsDose:
    data_dose.ix[row, 'scan date(YYYYMMDD)'] = dateconv(row)
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
        if (str(data_dose['scan date(YYYYMMDD)'][dose_row]) == str(data_rp['Date'][start].date()) and
                data_dose['series time'][dose_row] == data_rp['Injection Time'][start]):
            data_dose.ix[dose_row, 'ID'] = data_rp['ID'][start]
            data_dose.ix[dose_row, 'Row Index'] = int(start)
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
    if data_dose['scan date(YYYYMMDD)'][row_dose].year == 2010:
        loopMerge(row_dose, 0, 12)
    elif data_dose['scan date(YYYYMMDD)'][row_dose].year == 2011:
        loopMerge(row_dose, 13, 55)
    elif data_dose['scan date(YYYYMMDD)'][row_dose].year == 2012:
        loopMerge(row_dose, 56, 266)
    elif data_dose['scan date(YYYYMMDD)'][row_dose].year == 2013:
        loopMerge(row_dose, 267, 575)
    elif data_dose['scan date(YYYYMMDD)'][row_dose].year == 2014:
        loopMerge(row_dose, 576, 904)
    elif data_dose['scan date(YYYYMMDD)'][row_dose].year == 2015:
        loopMerge(row_dose, 905, 1173)
    else:
        loopMerge(row_dose, 1174, (num_rowsRp - 1))
    row_dose += 1
    



