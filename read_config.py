#! /usr/bin/env python

'''
Reads config file

returns dictionary of config variables -> values.
'''
def read_config() :
    import json
    config_file = 'config'
    fh = open(config_file, 'r')
    data = ''
    for line in fh :
        data = data + line.strip()
    fh.close()
    data = dict(json.loads(data))
    return data
