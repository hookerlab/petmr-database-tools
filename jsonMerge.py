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
    return str(dt)
    
#convert dose_info date to date format
row = 0
while row < num_rowsDose:
    data_dose.ix[row, 'scan date(YYYYMMDD)'] = dateconv(row)
    row += 1
    
'''
Year - Rows
2010 - 1-13
2011 - 14-56
2012 - 57-267
2013 - 268-576
2014 - 577-905
2015 - 906-num_rowsRp
'''
#Merge files based on Date and Time checks
row_dose = 0
row_rp = 0
while row_dose < num_rowsDose:
    while row_rp < num_rowsRp:
        if (str(data_dose['scan date(YYYYMMDD)'][row_dose]) == str(data_rp['Date'][row_rp].date()) and
                data_dose['series time'][row_dose] == data_rp['Injection Time'][row_rp]):
            for col in data_dose:
                if not col == 'quant_param':
                    data_rp.ix[row_rp, col] = data_dose[col][row_dose]
                else:
                    data_rp.set_value(row_rp, col, data_dose[col][row_dose])
            break
        row_rp += 1
    row_dose += 1
    



