#############################################################
#
# File Name: destination_ip
# Purpose: Contain methods to find, retrieve and
#          manipulate the destination ip address.
#
##############################################################

'''
    Method: get_destination_ip
    Purpose: Find and return destination IP address.
'''


def get_destination_ip_string(col_list):
    # Iterate over each list within list_of_column_values
    for ls in col_list:
        # Grab each value contained in each column
        for value in ls:
            if ('Destination' or 'destination') in str(value):
                return value

    return None


'''
    Method: get_destination_ip
    Purpose: Extract the destination IP from string
             and return the result.
'''


def get_destination_ip(string):
    # Split grab the actual ip address
    if '-' in string:
        return string.split(" - ")
    else:
        return string.split(" = ")
