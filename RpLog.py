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
#remove unneeded columns
data2 = data.drop(data.columns[18:], axis = 1)
print(list(data2))
#renamed Column 18 to Comments
data2.rename(columns={'Unnamed: 17': 'Comments'}, inplace=True)
print(list(data2))

# print(list(data2['SUBJECT'][0]))
# print(data2['SUBJECT'][0])
# print(data2['Time'][14])
# print(data2['Initial \n(mCi)'][14])
