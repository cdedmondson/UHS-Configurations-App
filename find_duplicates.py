#############################################################
#
# File Name: find_duplicates
# Purpose: Find duplicate serial numbers.
#
##############################################################


'''
    Method: find_duplicate_serial_numbers
    Purpose: Take in a dataframe as parameter
             and return sorted duplicate serial numbers.
'''


def find_duplicate_serial_numbers(dataframe):
    return dataframe[dataframe.index.duplicated(keep=False)].sort_index()
