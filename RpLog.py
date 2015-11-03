import pandas as pd
import json

__author__ = 'jphan'


# reads in excel file path
filename = input('Enter Path to file')
data = pd.read_csv(filename)
# data = pd.read_csv("RADIOPHARM log - Summary.csv")
#C:\Users\strike\Desktop\project\RADIOPHARM log - Summary.csv

# gets the number of rows
num_rows = len(data)

# holds a list of indexes with time formatting errors
errList = []

# title row
print("Total rows: {}".format(num_rows))
print(list(data))

# renaming Columns
data.rename(columns={' ': 'Date'}, inplace=True)
data.rename(columns={'Initial \n(mCi)': 'Initial (mCi)'}, inplace=True)
data.rename(columns={'Time': 'Initial Time'}, inplace=True)
data.rename(columns={'Residual\n(mCi)': 'Residual (mCi)'}, inplace=True)
data.rename(columns={'Time.1': 'Residual Time'}, inplace=True)
data.rename(columns={'Scan time/\nInjection time': 'Injection Time'}, inplace=True)
data.rename(columns={'Used\n(mCi)': 'Used (mCi)'}, inplace=True)
data.rename(columns={'Tracer\nAdmin.': 'Tracer Admin'}, inplace=True)
data.rename(columns={'C11/F18\nproduction': 'C11/F18 Production'}, inplace=True)
data.rename(columns={'Image\nAnalysis': 'Image Analysis'}, inplace=True)
data.rename(columns={'Blood\nAnalysis': 'Blood Analysis'}, inplace=True)
data.rename(columns={'Unnamed: 17': 'Comments'}, inplace=True)
print(list(data))

# changes all data in column to lowercase
data['SUBJECT'] = data['SUBJECT'].str.lower()
data['MANUF.'] = data['MANUF.'].str.lower()
data['Blood Analysis'] = data['Blood Analysis'].str.lower()
data['Image Analysis'] = data['Image Analysis'].str.lower()
data['C11/F18 Production'] = data['C11/F18 Production'].str.lower()
data['Initial (mCi)'] = data['Initial (mCi)'].str.lower()
data['Residual (mCi)'] = data['Residual (mCi)'].str.lower()

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

# checks if subject is one of the 4 options, used for debugging
# bo = True
# for dat in data['SUBJECT']:
#     if dat == 'human' or dat == 'animal' or dat == 'phantom' or dat == 'NULL':
#         bo = True
#     else:
#         bo = False
#         break

def boolConv(col):
    """ converts yes/no to 1/0
    Parameters:
    col: String
        Name of column
    Return:
    Out: Object
        Returns each row of the column as an object because there are cells that are 'NULL' from missing data
    """
    counts = 0
    for x in data[col]:
        if 'yes' in x:
            data.ix[counts, col] = int(1)
        elif 'no' in x:
            data.ix[counts, col] = int(0)
        counts += 1

#Calls boolConv function to convert yes/no to 1/0 according to the column
boolConv('Blood Analysis')
boolConv('Image Analysis')
boolConv('C11/F18 Production')

def dateconv(date):
    """ converts date mm/dd/yyyy to yyyy-mm-dd
    Parameters:
    date: String
        String of date of the current row in the 'Date' column
    Returns:
    Out: String
        Returns reformatted date yyyy-mm-dd
    """
    formtype = ['%m/%d/%y', '%m/%d/%Y']
    for f in formtype:
        try:
            dt = pd.datetime.strptime(data['Date'][date], f)
            break
        except ValueError:
            pass
    return str('{0}-{1}-{2}'.format(dt.year, dt.month, dt.day % 100))

# Reformats all the rows in dates to yyyy-mm-dd
x = 0
while x < num_rows:
    try:
        data.ix[x, 'Date'] = dateconv(x)
    except ValueError:
        if x not in errList:
            print(data['Date'][x])
            errList.append(x)
    x += 1

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

def allTimeConv(colName):
    """ converts all time data to 24hr format, indexes of times with errors are saved to errList
    Parameter:
    colName: String
        Name of column
    See Also:
    isTimeFormat(): checks if time is already in 24hr format
    timeconv(): converts time to 24hr format
    """
    y = 0
    while y < num_rows:
        curr = data[colName][y]
        timecheck = isTimeFormat(curr)
        if not (curr == 'NULL' or timecheck == True):
            try:
                data.ix[y, colName] = timeconv(colName, y)
            except ValueError:
                # print(y)
                if y not in errList:
                    errList.append(y)
                y += 1
        else:
            y += 1

# Calls allTimeConv to convert all time data for initial,residual, and TOI to 24hr format
allTimeConv('Initial Time')
allTimeConv('Residual Time')
allTimeConv('Injection Time')

# gets the unique values in a column
list_sub = pd.unique(data['SUBJECT'])
list_man = pd.unique(data['MANUF.'])
list_int = pd.unique(data['Initial (mCi)'])
list_res = pd.unique(data['Residual (mCi)'])

def findUni(inp):
    """ returns a list of unique non-number value
    Parameter:
    inp: Object
        List of unique values
    Return:
    Out: Object
        Returns a list of unique non-number values
    """
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

# finds unique non-number values and sorts the lists
uni_man = findUni(list_man)
uni_man.sort()
uni_int = findUni(list_int)
uni_int.sort()
uni_res = findUni(list_res)
uni_res.sort()

# concatenates the extra comments for columns 18 to 34
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

def commInit(colName, row):
    """ Moves unrelated data to comments and sets original position to 'NULL'
    Parameter:
    colName: String
        Name of column
    row: int
        Current row
    """
    if data[colName][row] != 'NULL':
        if data['Comments'][row] == 'NULL':
            data.ix[row, 'Comments'] = '"' + data[colName][row] + '"'
            data.ix[row, colName] = 'NULL'
        else:
            data.ix[row, 'Comments'] += ', "' + data[colName][row] + '"'
            data.ix[row, colName] = 'NULL'

def commMove(colName, uni_list):
    """ moves unrelated data to comments column
    Parameter:
    colName: String
        Name of column
    uni_list: Object
        List of unique values
    See Also:
    commInit: moves unique value to comment and sets original cell to 'NULL'
    """
    row = 0
    for x in data[colName]:
        for y in uni_list:
            if y in x:
                commInit(colName, row)
        row += 1

# moves unrelated non-number data to comments section
commMove('Initial (mCi)', uni_int)
commMove('Residual (mCi)', uni_res)

# relabels common manufactures to a common name
counts = 0
for x in data['MANUF.']:
    if 'cardinal' in x and 'pet' not in x:
        data.ix[counts, 'MANUF.'] = 'cardinal health'
    elif ('iba' in x or 'molec.' in x) and 'pet' not in x:
        data.ix[counts, 'MANUF.'] = 'i.b.a. molec'
    elif 'house' in x:
        data.ix[counts, 'MANUF.'] = 'in house'
    counts += 1

# drop unneeded columns
data = data.drop(['STUDY', 'PI'], axis=1)
data = data.drop(data.columns[16:], axis=1)

# saves modified data to csv file
writefile = pd.DataFrame(data)
writefile.to_csv('RADIOPHARM log - Summary_edited.csv', index=False, na_rep='NULL')

#creates JSON file of data
myJSON = data.to_json(path_or_buf=None, orient='index', date_format='epoch', double_precision=10, force_ascii=True,
                      date_unit='ms', default_handler=None)
print(myJSON)
with open('RadioPharmLog.json', 'w') as outfile:
    json.dump(myJSON, outfile)

# saves csv file of indexes with data error
errList.sort()
print(errList)
errIndex = pd.DataFrame(errList)
errIndex.columns = ['Error_Indexes']
errIndex.to_csv('Indexes_With_Errors.csv', index=False, na_rep='NULL')
