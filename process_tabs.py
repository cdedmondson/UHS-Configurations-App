#############################################################
#
# File Name: process_tabs
# Purpose: Handle all excel tab manipulation.
#
##############################################################

'''
    Method: get_excel_tabs_list
    Purpose: Get a list of excel file tabs.
'''


def get_excel_tabs_list(temp_dataframe):
    # Return excel tabs by utilizing the sheet_names attribute
    return temp_dataframe.sheet_names


'''
    Method: remove_unwanted_tabs
    Purpose: To remove invalid/unwanted tabs.
'''


def remove_unwanted_tabs(tabs_list):
    valid_tabs = []

    for tab in tabs_list:
        if 'Appliance' in tab:
            valid_tabs.append(tab)

    return valid_tabs


'''
    Method: select_tab_by_index
    Purpose: Take in excel tabs list and index user wants to select
             and return results.
'''


def select_tab_by_index(index, tabs_list):
    # Return selected tab(s)
    return tabs_list[index]


'''
    Method: read_single_tab_into_dataframe
    Purpose: Read excel sheet, select a specific tab by the tabs name,
             and specify what column to use as index/key
'''


def read_single_tab_into_dataframe(tab_to_select, dataframe):
    return dataframe.parse(tab_to_select)
