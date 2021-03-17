import logging
from constants import COMP_ERROR

#NOTE:- Formats Bytes size into GB,MB, & kb
def format_size(num):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, "B")
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', "B")