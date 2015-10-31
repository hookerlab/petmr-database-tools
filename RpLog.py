import pandas as pd
__author__ = 'jphan'

#read in excel file
data = pd.read_csv("RADIOPHARM log - Summary-mod.csv")

#get number of rows
num_rows = len(data)

#title row
print("Total rows: {}".format(num_rows))
print(list(data))

#rename first column title to Date
data.rename(columns={' ': 'Date'}, inplace=True)
print(list(data))

#drop unneeded column
data2 = data.drop(['STUDY', 'PI'], axis=1)

#renamed Columns
data2.rename(columns={'Unnamed: 17': 'Comments'}, inplace=True)
data2.rename(columns={'Time': 'Initial_Time'}, inplace=True)
data2.rename(columns={'Time.1': 'Residual_Time'}, inplace=True)
data2.rename(columns={'Scan time/\nInjection time': 'TOI'}, inplace=True)
# data2.rename(columns={'Unnamed: 34': 'Indicies_With_Error'}, inplace=True)
print(list(data2))

#changes data in column to lowercase
data2['SUBJECT'] = data2['SUBJECT'].str.lower()
data2['MANUF.'] = data2['MANUF.'].str.lower()
data2['Blood\nAnalysis'] = data2['Blood\nAnalysis'].str.lower()
data2['Image\nAnalysis'] = data2['Image\nAnalysis'].str.lower()
data2['C11/F18\nproduction'] = data2['C11/F18\nproduction'].str.lower()

#fills in empty cells
data2.fillna(value = 'NULL',inplace=True)

#change yes/no to boolean 1/0                         PROBLEM RETURNS A DOUBLE INSTEAD OF INT IN CONSOLE BUT NOT EXCEL??
aboolean = {'yes': 1, 'no': 0}
data2['Blood\nAnalysis'] = data2['Blood\nAnalysis'].map(aboolean)

data2['Image\nAnalysis'] = data2['Image\nAnalysis'].map(aboolean)

data2['C11/F18\nproduction'] = data2['C11/F18\nproduction'].map(aboolean)

#converts date mm/dd/yyyy to yyyy-mm-dd
def dateconv(date):
    dt = pd.datetime.strptime(data2['Date'][date], '%m/%d/%Y')
    return str('{0}-{1}-{2}'.format(dt.year, dt.month, dt.day % 100))

#converts all the data dates
x = 0
while x < num_rows:
    data2.ix[x, 'Date'] = dateconv(x)
    x += 1

#convert 12 hr to 24 hr
def timeconv(colName, time):
    return str(pd.datetime.strptime(data2[colName][time], '%I:%M:%S %p').time())

#checks if time is already in 24hr format
def isTimeFormat(input):
    try:
        pd.datetime.strptime(input, '%H:%M:%S').time()
        return True
    except ValueError:
        return False

#holds list of indexes with time formatting errors
errList = []
def allTimeConv(colName):
    #converts all time data to 24hr format, indexes of times with errors are saved to errList
    y = 0
    while y < num_rows:
        curr = data2[colName][y]
        timecheck = isTimeFormat(curr)
        if not(curr == 'NULL' or curr == 'N/A' or curr == 'n/a' or curr == 'N/a' or curr == 'n/A' or timecheck == True):#ON THIS PART FIND HOW TO FIX ROW 47 already in mil time
            try:
                data2.ix[y, colName] = timeconv(colName, y)
            except ValueError:
                # print(y)
                if y not in errList:
                    errList.append(y)
                y += 1
        else:
            y += 1

#converts all time data for initial,residual, and TOI
allTimeConv('Initial_Time')
allTimeConv('Residual_Time')
allTimeConv('TOI')
errList.sort()

#check for anagram - for Manuf/etc
def anagramSolution4(s1, s2):
    c1 = [0]*26
    c2 = [0]*26
    for i in range(len(s1)):
        pos = ord(s1[i]) - ord('a')
        if pos >= 0:
            c1[pos] += 1
    for i in range(len(s2)):
        pos = ord(s2[i])-ord('a')
        if pos >= 0:
            c2[pos] += 1
    j = 0
    stillOK = True
    while j<26 and stillOK:
        if c1[j]==c2[j]:
            j = j + 1
        else:
            stillOK = False
    return stillOK


#save a csv file with a list of indexes with errors        
# errIndex = pd.DataFrame(errList)
# errIndex.columns = ['Error_Indexes']
# errIndex.to_csv('Indexes_With_Errors.csv', index=False, na_rep = 'null' )

#saves a csv file the data
# test = pd.DataFrame(data2)
# test.to_csv('test2.csv', index=False, na_rep = 'null' )
