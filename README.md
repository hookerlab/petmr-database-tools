# petmr-database-tools
Used Python 3.4.3, Pandas 0.16.2

##RpLog.py does:

1.Renames columns to have meaningful names and avoid returns(\n, next line)

2.Replaces empty cells/missing infomation with 'NULL'

3.Can check if 'Subjects' is one of the following 'human,animal,phantom,or NULL'

4.Converts 'Yes/No' to 1/0 for columns: Blood Analysis, Image Analysis, C11/F18 Production

5.Converts dates to yyyy-mm-dd format

6.Converts time to 24hr(military) format for columns: Initial Time, Residual Time, TOI

7.Concatenates extra columns with data to Comments column

8.Moves any non-related data(non-number) in Initial and Residual Columns to comments column

9.Relabels common names with minor differences (ie. in house / in-house) to a common name (ie in house)

10.Drops unneeded columns before outputing

11.Creates:

  -CSV file of edited columns/data
    
  -JSON file of the data
    
  -CSV file with indexes of columns that has errors
  
## doseInfoOneJSONFile.py does:
1.Recieves input from user for starting directory to create a list of paths to all Dose_info.xls files

2.For each xls file,
  
  -fill empty cells with 'NULL'
  
  -Check + modify any value with a time to 24hr format
  
  -Concatenates quant_param values into 1 cell
  
  -creates empty row at the bottom
    -Reason: Allows the script to access the 'Calibration Time' value. If there is no value for 'Calibration Time', pyhton reads the number of rows as 24 giving an error when trying to access that cell, while xls files with a 'Calibration Time' will have 25 rows.
    
  -Check if 'Blood Pressure' has a valid value
  
3.Gathers specified data into an ordered dictionary

4.Creates JSON file contain objects for all found 'Dose_info.xls' files 

