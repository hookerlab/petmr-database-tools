""" doseInfo1jsonFile.py

    Usage:
        doseInfo1jsonFile.py
        doseInfo1jsonFile.py [<Dose_info_Path>]

    Options:
        Dose_info_Path      : Path to Dose_info.json
"""
from docopt import docopt
import pandas as pd
import json
import os
from collections import OrderedDict
import re

__author__ = 'jphan'
'''
Manipulates 'Dose_info.xls' data to required format
Outputs:
-JSON file of data
'''
#Gets starting directory to find dose_info.xls files
pathname = ''
if __name__ == "__main__":
    args = docopt(__doc__)
    boo = False
    if args["<Dose_info_Path>"]:
        pathname = str(args["<Dose_info_Path>"])
        pathname = pathname.strip()
        boo = True

    elif boo == False:
        pathname = input('Enter Path to files: ')
        pathname = pathname.strip()
    pathList = []
    dirList = []
    dirNameList = []
    fnameList = []
    for dirName, subdirList, fileList in os.walk(pathname):
        currdir = os.path.basename(dirName)
        for fname in fileList:
            if 'Dose_info.xls' in fname:
                pathList.append(os.path.join(dirName, fname))
                dirList.append(dirName)
                dirNameList.append(currdir)
                nam = os.path.splitext(fname)[0]
                fnameList.append(nam)

    #list of indexes with errors
    errList = []

    def isTimeFormat(input):
        """ checks if time is already in 24hr format
        Parameter:
        input: String
            String of the time input
        Returns:
        Out: Boolean
            True: if time string is already in 24hr format
            False: if time string is not in 24hr format
        """
        try:
            pd.datetime.strptime(input, '%H:%M:%S').time()
            return True
        except ValueError:
            return False

    def timeconv(colName, row):
        """ convert 12 hr to 24 hr
        Parameters:
        colName: String
            Name of column
        row: String
            Current row in the column
        Return:
        Out: String
            Returns the time in 24hr format
        """
        return str(pd.datetime.strptime(data[colName][row], '%I:%M:%S %p').time())

    doseList = []
    c = 0
    while c < len(pathList):
        # reads in excel file path from list
        data = pd.read_excel(pathList[c], header=None)

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

        #list of col and row index for each time cell
        time_col_list = [1, 1, 3, 7, 7]
        time_row_list = [2, 3, 2, 2, 6]
        listlen = len(time_col_list)

        #loops through each cell with a time value and convert if needed to 24hr format
        counter = 0
        while counter < listlen:
            data[time_col_list[counter]][time_row_list[counter]] = str(data[time_col_list[counter]][time_row_list[counter]])
            curr = data[time_col_list[counter]][time_row_list[counter]]
            timecheck = isTimeFormat(curr)
            if not (curr == 'NULL' or timecheck == True):
                try:
                    data.ix[time_row_list[counter], time_col_list[counter]] = timeconv(time_col_list[counter], time_row_list[counter])
                    counter += 1
                except ValueError:
                    if counter not in errList:
                        errList.append(counter)
                    counter += 1
            else:
                counter += 1

        #creates string to hold quant_param values
        quant_param = []
        num = 1
        boo = False
        #creates list
        while num < 5:
            quant_param.append(data[num][0])
            num += 1
        data.set_value(1, 1, quant_param)

        #creates a new empty row at the end
        newrow = []
        lencol = len(data.columns)
        count = 0
        var = 'NULL'
        while count < lencol:
            newrow.append(var)
            count += 1
        data.loc[len(data)] = newrow

        #checks if blood pressure has a number
        def hasNumbers(inputString):
            """
            Parameter:
            inputString: String

            Return:
            Out: Boolean
                True if there is a number in the input
                False if there is no number in the input
            """
            return bool(re.search(r'\d', inputString))

        #changes the value of blood pressure to 'NULL' if invalid value
        if hasNumbers(data[7][13]) == False:
            data.ix[13, 7] = 'NULL'

        #gathers specified data
        dose = OrderedDict()
        dose['quant_param'] = data[1][1]
        dose['series time'] = data[1][2]
        dose['acquisition time'] = data[1][3]
        dose['toi'] = data[3][2]
        dose['initial activity'] = data[7][1]
        dose['calibration time'] = data[7][2]
        dose['residual activity'] = data[7][5]
        dose['residual time'] = data[7][6]
        dose['blood gluc'] = data[7][12]
        dose['blood pressure'] = data[7][13]
        dose['pulse'] = data[7][14]
        dose['calibration_Cs_137'] = data[7][17]
        dose['calibration_Co_57'] = data[7][18]
        dose['patient weight'] = data[9][1]
        dose['patient height'] = data[9][4]
        dose['patient sex'] = data[9][7]
        dose['patient birth year(YYYY)'] = data[9][10]
        dose['scan date(YYYYMMDD)'] = data[9][13]
        dose['reconstruction date'] = data[9][16]
        dose['reconstruction time'] = data[9][19]
        dose['calibration date'] = data[9][22]
        dose['calibration time'] = data[9][25]
        doseList.append(dose)
        c += 1

    #creates JSON file of specified data
    j = json.dumps(doseList)
    #Saves JSON files to 1 specified directory
    savePath = input('Enter save directory path: ')
    savePath = savePath.strip()
    completeName = os.path.join(savePath, 'Dose_info.json')
    with open(completeName, 'w') as f:
        f.write(j)
