#############################################################
#
# File Name: process_columns
# Purpose: Handle all column manipulation.
#
##############################################################


'''
    Method: get_excel_columns_list
    Purpose: Return a list of the dataframe's columns.
'''


def get_excel_columns_list(dataframe):
    return dataframe.columns


'''
    Method: check_pocmonitor_name
    Purpose: Make sure the column labeled pocmintor_sn
             does not have any typos. If it does update column with correct name.
'''


def check_pocmonitor_name(list_of_columns):
    for column in list_of_columns:
        if ('pocmonitor_sn' in column) and column != 'pocmonitor_sn':
            return column

    return 'pocmonitor_sn'


'''
    Method: get_empty_columns
    Purpose: Return a list of columns that contain no
             no data i.e. have to purpose.
'''


def get_empty_columns(cols_list):
    drop_cols = []
    # Loop over each column name
    for col in cols_list:
        # If 'Unnamed:' is contained in the column name append to the list
        if 'Unnamed:' in col:
            drop_cols.append(col)

    return drop_cols


'''
    Method: get_unwanted_column_values
    Purpose: Return values contained in unwanted columns.
'''


def get_unwanted_column_values(cols_to_obtain_values, dataframe):
    cols_elements = []
    for col in cols_to_obtain_values:
        # Create a list of unwanted columns and their values/elements
        cols_elements.append(dataframe[col].values)

    return cols_elements


'''
    Method: drop_unwanted_columns
    Purpose: Drop columns that have no data or data
             that is no longer needed.
'''


def drop_unwanted_columns(dataframe, cols_to_drop):
    # Drop all unwanted columns from dataframe
    for col in cols_to_drop:
        # Inplace=True make change permanent
        # Axis=1 select only columns
        dataframe.drop(str(col), inplace=True, axis=1)


'''
    Method: create_destination_ip_column
    Purpose: Create destination_ip column and
             insert the ip as values.
'''


def create_destination_ip_column(dest_ip, dataframe):
    dataframe['destination_ip'] = str(dest_ip[1])
