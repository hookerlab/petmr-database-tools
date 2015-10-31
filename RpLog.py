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

# print(data2['ID'][12])
# print(data2['ID'][14])
#fills in empty cells
data2.fillna(value = 'NULL',inplace=True)

#change yes/no to boolean 1/0                         PROBLEM RETURNS A DOUBLE INSTEAD OF INT IN CONSOLE BUT NOT EXCEL??
aboolean = {'Yes': 1, 'No': 0}
data2['Blood\nAnalysis'] = data2['Blood\nAnalysis'].map(aboolean)

data2['Image\nAnalysis'] = data2['Image\nAnalysis'].map(aboolean)

data2['C11/F18\nproduction'] = data2['C11/F18\nproduction'].map(aboolean)

#converting date
def dateconv(date):
    dt = pd.datetime.strptime(data2['Date'][date], '%m/%d/%Y')
    return str('{0}-{1}-{2}'.format(dt.year, dt.month, dt.day % 100))

#converts all the data dates
x = 0
while x < num_rows:
    data2.ix[x, 'Date'] = dateconv(x)
    x += 1

#converts 12hr format to mil time
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
