# Project-Radiopharm_Log
Used Python 3.4.3, Pandas 0.16.2

RpLog.py does:

1.Renames columns to have meaningful names and avoid returns(\n, next line)

2.Replaces empty cells/infomation with 'NULL'

3.Can check 'Subjects' to be one of the following 'human,animal,phantom,or NULL'

4.Converts 'Yes/No' to 1/0 for columns: Blood Analysis, Image Analysis, C11/F18 Production

5.Converts dates to yyyy-mm-dd format

6.Converts time to 24hr(military) format

7.Concatenates extra columns with data to Comments column

8.Moves any non-related data(non-number) in Initial and Residual Columns

9.Relabels common names with minor differences (ie. in house / in-house) to a common name (ie in house)

10.Drops unneeded columns before outputing to JSON file

11.Creates CSV file of edited columns

12.Creates JSON file of the data

13.Creates CSV file with indexes of columns that has errors
