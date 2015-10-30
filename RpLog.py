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
bloodanaly = {'Yes': 1, 'No': 0}
data2['Blood\nAnalysis'] = data2['Blood\nAnalysis'].map(bloodanaly)

imageanaly = {'Yes': 1, 'No': 0}
data2['Image\nAnalysis'] = data2['Image\nAnalysis'].map(imageanaly)

produc = {'Yes': 1, 'No': 0}
data2['C11/F18\nproduction'] = data2['C11/F18\nproduction'].map(produc)

#converting date
dt = pd.datetime.strptime(data2['Date'][0], '%m/%d/%Y')
print ('{0}-{1}-{2}'.format(dt.year, dt.month, dt.day % 100))

test = pd.DataFrame(data2)
test.to_csv('test2.csv', index=False, na_rep = 'null' )
