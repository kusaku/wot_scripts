# Embedded file name: scripts/common/bwdebug.py
import BigWorld
import sys
printPath = False

def getClassName(f):
    try:
        selfClass = f.f_locals['self'].__class__
        try:
            mro = selfClass.__mro__
        except AttributeError:
            stack = [selfClass]
            mro = []
            while stack:
                curr = stack.pop(0)
                mro.append(curr)
                stack += curr.__bases__

        funcName = f.f_code.co_name
        for c in mro:
            try:
                if funcName.startswith('__'):
                    method = c.__dict__['_' + c.__name__ + funcName]
                else:
                    method = c.__dict__[funcName]
                if method.func_code == f.f_code:
                    return c.__name__ + '.'
            except KeyError:
                pass

    except:
        pass

    return ''


def defaultOutputMethod(arg1, arg2):
    pass


def _printMessage(outputMethod, args, printPath):
    f = sys._getframe(2)
    output = ''
    if printPath:
        output += f.f_code.co_filename + '(' + str(f.f_lineno) + ') : '
    output += getClassName(f) + f.f_code.co_name + ': '
    output += ' '.join([ str(m) for m in args ])
    outputMethod('', output)


def getOutputMethod(method):
    if not hasattr(BigWorld, method):
        return defaultOutputMethod
    return getattr(BigWorld, method)


def TRACE_MSG(*args):
    _printMessage(getOutputMethod('logTrace'), args, printPath)


def DEBUG_MSG(*args):
    _printMessage(getOutputMethod('logDebug'), args, printPath)


def INFO_MSG(*args):
    _printMessage(getOutputMethod('logInfo'), args, printPath)


def NOTICE_MSG(*args):
    _printMessage(getOutputMethod('logNotice'), args, printPath)


def WARNING_MSG(*args):
    _printMessage(getOutputMethod('logWarning'), args, True)


def ERROR_MSG(*args):
    _printMessage(getOutputMethod('logError'), args, True)


def CRITICAL_MSG(*args):
    _printMessage(getOutputMethod('logCritical'), args, True)


def HACK_MSG(*args):
    _printMessage(getOutputMethod('logHack'), args, True)