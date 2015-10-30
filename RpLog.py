import pandas as pd
__author__ = 'jphan'

#read in excel file
# data = pd.read_csv("RADIOPHARM log - Summary-mod.csv")
data = pd.read_csv("RADIOPHARM log - Summary-mod_debug.csv")

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

# print(data2['ID'][12])
# print(data2['ID'][14])

# print(list(data2['SUBJECT'][0]))
# print(data2['SUBJECT'][0])
# print(data2['Time'][14])
# print(data2['Initial \n(mCi)'][14])
# print(list(data2['Time'][2]))
# print(len(data2['Time'][2]))


test = pd.DataFrame(data2)
test.to_csv('test2.csv', index=False, na_rep = 'null' )
