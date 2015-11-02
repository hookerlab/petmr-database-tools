import pandas as pd
import json
import csv
__author__ = 'jphan'

#read in excel file
data = pd.read_csv("RADIOPHARM log - Summary-mod.csv")

#get number of rows
num_rows = len(data)

#holds list of indexes with time formatting errors
errList = []

#title row
print("Total rows: {}".format(num_rows))
print(list(data))

#renamed Columns
data.rename(columns={' ': 'Date'}, inplace=True)
data.rename(columns={'Initial \n(mCi)': 'Initial (mCi)'}, inplace=True)
data.rename(columns={'Time': 'Initial Time'}, inplace=True)
data.rename(columns={'Residual\n(mCi)': 'Residual (mCi)'}, inplace=True)
data.rename(columns={'Time.1': 'Residual Time'}, inplace=True)
data.rename(columns={'Scan time/\nInjection time': 'Injection Time'}, inplace=True)
data.rename(columns={'Used\n(mCi)': 'Used (mCi)'}, inplace=True)
data.rename(columns={'Tracer\nAdmin': 'Tracer Admin'}, inplace=True)
data.rename(columns={'C11/F18\nproduction': 'C11/F18 Production'}, inplace=True)
data.rename(columns={'Image\nAnalysis': 'Image Analysis'}, inplace=True)
data.rename(columns={'Blood\nAnalysis': 'Blood Analysis'}, inplace=True)
data.rename(columns={'Unnamed: 17': 'Comments'}, inplace=True)

#changes data in column to lowercase
data['SUBJECT'] = data['SUBJECT'].str.lower()
data['MANUF.'] = data['MANUF.'].str.lower()
data['Blood Analysis'] = data['Blood Analysis'].str.lower()
data['Image Analysis'] = data['Image Analysis'].str.lower()
data['C11/F18 Production'] = data['C11/F18 Production'].str.lower()
data['Initial (mCi)'] = data['Initial (mCi)'].str.lower()
data['Residual (mCi)'] = data['Residual (mCi)'].str.lower()

#fills in empty cells
data.fillna(value='NULL', inplace=True)
temp = 0
nalist = ['n/a', 'N/A', 'N/a', 'n/A']
while temp < num_rows:
    for col in data.ix[:, 0:17]:
        for y in nalist:
            if y == data[col][temp]:
                data.ix[temp, col] = 'NULL'
                break
    temp += 1
    
#checks if subject is one of the 4 options
bo = True
for dat in data['SUBJECT']:
    if dat == 'human' or dat == 'animal' or dat == 'phantom' or dat == 'NULL':
        bo = True
    else:
        bo = False
        break

#change yes/no to boolean 1/0
aboolean = {'yes': 1, 'no': 0}
data['Blood Analysis'] = data['Blood Analysis'].map(aboolean)
data['Image Analysis'] = data['Image Analysis'].map(aboolean)
data['C11/F18 Production'] = data['C11/F18 Production'].map(aboolean)

#converts date mm/dd/yyyy to yyyy-mm-dd
def dateconv(date):
    dt = pd.datetime.strptime(data['Date'][date], '%m/%d/%Y')
    return str('{0}-{1}-{2}'.format(dt.year, dt.month, dt.day % 100))

#converts all the data dates
x = 0
while x < num_rows:
    data.ix[x, 'Date'] = dateconv(x)
    x += 1

#checks if time is already in 24hr format
def isTimeFormat(input):
    try:
        pd.datetime.strptime(input, '%H:%M:%S').time()
        return True
    except ValueError:
        return False

#convert 12 hr to 24 hr
def timeconv(colName, time):
    return str(pd.datetime.strptime(data[colName][time], '%I:%M:%S %p').time())

#converts all time data to 24hr format, indexes of times with errors are saved to errList
def allTimeConv(colName):
    y = 0
    while y < num_rows:
        curr = data[colName][y]
        timecheck = isTimeFormat(curr)
        if not(curr == 'NULL' or timecheck == True):
            try:
                data.ix[y, colName] = timeconv(colName, y)
            except ValueError:
                # print(y)
                if y not in errList:
                    errList.append(y)
                y += 1
        else:
            y += 1

#converts all time data for initial,residual, and TOI
allTimeConv('Initial Time')
allTimeConv('Residual Time')
allTimeConv('Injection Time')

#gets unique values in a column
list_sub = pd.unique(data['SUBJECT'])
list_man = pd.unique(data['MANUF.'])
list_int = pd.unique(data['Initial (mCi)'])
list_res = pd.unique(data['Residual (mCi)'])

#returns a list of unique non number entries
def findUni(inp):
    tempList = []
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for x in inp:
        for y in alpha:
            if y in x:
                if x not in tempList:
                    tempList.append(x)
                    break
    return tempList

#finds unique non number and sorts
uni_man = findUni(list_man)
uni_man.sort()
uni_int = findUni(list_int)
uni_int.sort()
uni_res = findUni(list_res)
uni_res.sort()

#concatenates the extra comments
comm_loc = data.columns.get_loc("Comments")
temp = 0
while temp < num_rows:
    for col in data.ix[:, comm_loc + 1:]:
        if data['Comments'][temp] != 'NULL':
            if data[col][temp] != 'NULL':
                data.ix[temp, 'Comments'] += ', "' + str(data[col][temp]) + '"'
        else:
            if data[col][temp] != 'NULL':
                data.ix[temp, 'Comments'] = '"' + str(data[col][temp]) + '"'
    temp += 1

#swaps unrelated data to comments
def commInit(colName, count):
    if data[colName][count] != 'NULL':
        if data['Comments'][count] == 'NULL':
            data.ix[count, 'Comments'] = '"' + data[colName][count] + '"'
            data.ix[count, colName] = 'NULL'
        else:
            data.ix[count, 'Comments'] += ', "' + data[colName][count] + '"'
            data.ix[count, colName] = 'NULL'

#moves random data to comments column
def commMove(colName, uni_list):
    counter = 0
    for x in data[colName]:
        for y in uni_list:
            if y in x:
                commInit(colName, counter)

        counter += 1

#moves unrelated non number data to comments section
commMove('Initial (mCi)', uni_int)
commMove('Residual (mCi)', uni_res)

#relabels common manufactures to a common name
counts = 0
for x in data['MANUF.']:
    if 'cardinal' in x:
        data.ix[counts, 'MANUF.'] = 'cardinal health'
    elif 'iba' in x or 'molec.' in x:
        data.ix[counts, 'MANUF.'] = 'i.b.a. molec'
    elif 'house' in x:
        data.ix[counts, 'MANUF.'] = 'in house'
    counts += 1

#drop unneeded column
data = data.drop(['STUDY', 'PI'], axis=1)
data = data.drop(data.columns[18:], axis=1)
print(list(data))

#saves to csv file
# writefile = pd.DataFrame(data)
# writefile.to_csv('final_edited.csv', index=False, na_rep='null')

#saves csv file of indexes with data error
# errList.sort()
# errIndex = pd.DataFrame(errList)
# errIndex.columns = ['Error_Indexes']
# errIndex.to_csv('Indexes_With_Errors.csv', index=False, na_rep='null')
