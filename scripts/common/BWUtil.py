# Embedded file name: scripts/common/BWUtil.py
import ResMgr
from bwdebug import TRACE_MSG
from functools import partial
import sys, os
try:
    orig_open = __builtins__['open']
except TypeError as e:
    orig_open = __builtins__.open

@partial
def bwResRelativeOpen(name, *args):
    """
    This method has been decorated with 'partial' to avoid using a function as 
    a bound method when stored as a class attribute (see WOWP-638). """
    try:
        name = ResMgr.resolveToAbsolutePath(name).decode('utf8')
    except Exception as e:
        raise IOError(2, str(e))

    return orig_open(name, *args)


def monkeyPatchOpen():
    TRACE_MSG('BWUtil.monkeyPatchOpen: Patching open()')
    try:
        __builtins__['open'] = bwResRelativeOpen
    except TypeErorr as e:
        __builtins__.open = bwResRelativeOpen


def extendPath(path, name):
    """Extend path, this method is based on pkgutil.extend_path and will
    allow aid on supporting inheriting resource paths.
    
    Example usage:
    from BWUtil import extendPath
    __path__ = extendPath(__path__, __name__)
    """
    from pkgutil import extend_path
    path = extend_path(path, name)
    if not isinstance(path, list):
        return path
    pname = os.path.join(*name.split('.'))
    init_py = '__init__' + os.extsep + 'py'
    path = path[:]
    for dir in sys.path:
        if not isinstance(dir, basestring) or not ResMgr.isDir(dir):
            continue
        subdir = os.path.join(dir, pname)
        initfile = os.path.join(subdir, init_py)
        if subdir not in path and ResMgr.isFile(initfile):
            path.append(subdir)

    return path