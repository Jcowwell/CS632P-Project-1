import logging
from constants import COMP_ERROR

#NOTE:- Formats Bytes size into GB,MB, & kb
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except Exception:
        logging.error(COMP_ERROR)
        return "0.0"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2f GB" % (G)
        else:
            return "%.2f MB" % (M)
    else:
        return "%.2f kb" % (kb)