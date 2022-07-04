#############################################################
#
# File Name: file_handler
# Purpose: handle all file reading and writing functions.
#
##############################################################
import pandas as pd

'''
    Method: read_entire_excel_file
    Purpose: Take in the file to be read absolute file path, then read  
             the entire excel file into a pandas dataframe - including all tabs.
'''


def read_entire_excel_file(file_path):
    # Return dataframe
    return pd.ExcelFile(file_path)


'''
    Method: write_to_csv_file
    Purpose: Take in a pandas dataframe, file, 'mode' i.e. append 
             or write, and header then write the file to disk.
'''


def write_to_csv_file(dataframe, file, mode='w', header=True):
    return dataframe.to_csv(file, mode=mode, header=header)


'''
    Method: write_to_excel_file
    Purpose: Take in a pandas dataframe, file, 'mode' i.e. append 
             or write, and header then write the file to disk.
'''


def write_to_excel_file(dataframe, file, mode='w', header=True):
    return dataframe.to_excel(file, mode, header)
