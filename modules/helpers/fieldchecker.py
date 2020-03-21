'''
Check config.ini field values to check if valid
'''

import re

# TODO: Need to check only mandatory fields
def FieldCheck(field, value, debug=False):
    '''
    Check config.ini field values to check if valid
    '''

    # General fields

    if field == "wlan_if":
        valid_fields = [ 'wlan0', 'wlan1', 'wlan2' ]
        if value in valid_fields: return True
        return False
    
    if field == 'platform':
        valid_fields = [ 'rpi', 'wlanpi']
        if value in valid_fields: return True
        return False
    
    if field == 'data_format':
        valid_fields = [ 'csv', 'json']
        if value in valid_fields: return True
        return False

    if field == 'data_dir':
        return True
    
    if field == 'data_transport':
        valid_fields = [ 'hec', 'forwarder']
        if value in valid_fields: return True
        return False

    if field == 'data_host':
        if re.match("\d+?\.\d+?\.\d+?\.\d+", value): return True
        if re.match("\w+", value): return True
        return False
    
    if field == 'splunk_token':
        if re.match("^[\w|\-]{36}$", value): return True
        return False
    
    # Speedtest fields
    if field == 'speedtest_enabled':
        valid_fields = [ 'yes', 'no']
        if value in valid_fields: return True
        return False

    if field == 'speedtest_data_file':
        if value == '': return False
        return True

    return True
