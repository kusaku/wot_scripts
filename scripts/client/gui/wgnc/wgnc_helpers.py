# Embedded file name: scripts/client/gui/wgnc/wgnc_helpers.py
from debug_utils import LOG_ERROR

def parseSize(sizeStr):
    if sizeStr:
        try:
            size = map(int, sizeStr.split('x'))
            if len(size) != 2:
                raise ValueError
        except ValueError:
            LOG_ERROR('Failed to parse size: %s' % sizeStr)
            size = None

    else:
        size = None
    return size