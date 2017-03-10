#!/usr/bin/python

#
# Python script fine tune the format of a CMPIS 3.11 ETL extract, del file.
# Pete Jansz 03-10-2017
# 

#from subprocess import Popen, PIPE

try:
    import os
    import os.path
    import string
    import sys
    import optparse
    from os import chdir
    import logging
    import re
    import sys

except ImportError:
    sys.stderr.write('update_del_file.py' + ' ' + str(sys.exc_type) +
                     ' ' + str(sys.exc_value) + '\n')
    sys.exit(sys.exc_value)

SCRIPT_NAME = 'update_del_file.py'
PROG_BANNER = SCRIPT_NAME + ' v3.11.0\n\n'
PROG_BANNER += "\n  USAGE: %s -del_filename <filename>\n" % (SCRIPT_NAME)
DELIMITER = chr(11)

def show_usage():
    "show_usage(): Print program version, usage info to stderr and exit.__doc__"
    sys.stderr.write(PROG_BANNER)
    sys.exit(1)

def format_file(del_filename):
    format_map = make_format_map(del_filename)
    formatted_ouput = format(del_filename, format_map)
    write_file(del_filename, formatted_ouput)

def make_format_map(del_filename):

    format_filename = del_filename.replace('.del', '.format')
    format_map = {}
    for line in open(format_filename).readlines():
        (key, value) = line.split(':')
        format_map[key] = value.strip()

    return format_map

def format(del_filename, format_map):  # BIG string

    formatted_output = ''
    format_str = None

    for row in open(del_filename).readlines():
        if row.find(DELIMITER) == -1:
            continue

        data_items = row.rstrip().split(DELIMITER)
        
        if format_str == None:
            format_str = build_format_str(data_items, format_map)

        formatted_row = format_str % tuple( data_items )
        formatted_output += formatted_row

    return formatted_output

def build_format_str(data_items, format_map):  # format_str
    format_str = ''
    
    if len(format_map.keys()) == 0:
        format_str = DELIMITER.join(map(str, data_items))
    else:
        list = []
        for col_nr in range(1, len(data_items)+1):
        
            format_map_key = "c%s" % col_nr
            format_spec = None

            if format_map_key in format_map:
                format_spec = format_map[format_map_key]

            if format_spec != None:
                list.append(format_spec)
            else:
                list.append("%s")
        
        format_str = DELIMITER.join(map(str, list))
        
    return format_str + "\n"

def write_file(del_filename, data):
    file = open(del_filename, 'w')
    file.write(data)
    file.close()
    
def main():
    parser = optparse.OptionParser()

    parser.add_option('-d', '--del_filename',
                      action="store", dest="del_filename",
                      help="delimited filename")

    arg_values, args = parser.parse_args()

    if os.path.exists(arg_values.del_filename):
        format_file(os.path.abspath(arg_values.del_filename))


if __name__ == "__main__":
    main()
