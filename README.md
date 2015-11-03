# Project-Radiopharm_Log

RpLog.py does:
-Renames columns to have meaningful names and avoid returns(\n, next line)
-Replaces empty cells/infomation with 'NULL'
-Can check 'Subjects' to be one of the following 'human,animal,phantom,or NULL'
-Converts 'Yes/No' to 1/0 for columns: Blood Analysis, Image Analysis, C11/F18 Production
-Converts dates to yyyy-mm-dd format
-Converts time to 24hr(military) format
-Concatenates extra columns with data to Comments column
-Moves any non-related data(non-number) in Initial and Residual Columns
-Relabels common names with minor differences (ie. in house / in-house) to a common name (ie in house)
-Drops unneeded columns before outputing to JSON file
-Creates CSV file of edited columns
-Creates JSON file of the data
-Creates CSV file with indexes of columns that has errors
