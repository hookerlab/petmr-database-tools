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
data2 = data.drop(['STUDY'], axis = 1)

#renamed Column 18 to Comments
data2.rename(columns={'Unnamed: 17': 'Comments'}, inplace=True)
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
def timeconv(time):
    return str(pd.datetime.strptime(data2['Time'][time], '%I:%M:%S %p').time())

#checks if time is already in 24hr format
def isTimeFormat(input):
    try:
        pd.datetime.strptime(input, '%H:%M:%S').time()
        return True
    except ValueError:
        return False

test = pd.DataFrame(data2)
test.to_csv('test2.csv', index=False, na_rep = 'null' )
