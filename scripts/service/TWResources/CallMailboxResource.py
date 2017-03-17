# Embedded file name: scripts/service/TWResources/CallMailboxResource.py
import functools
from twisted.web import resource, server
from json_util import JSONResource, ErrorPage, sendJSON, sendJSONError
from arg_convert import convertArgs
import KeepAliveMailboxes
import BWTwoWay

class TwoWayCallResource(JSONResource):

    def __init__(self, method = None, filterFn = None):
        JSONResource.__init__(self)
        self.method = method
        self.filterFn = filterFn
        raise filterFn is None or callable(filterFn) or AssertionError
        return

    def _renderResponse(self, request, response):
        if self.filterFn:
            result = self.filterFn(response)
        else:
            result = self.method.convertReturnValuesToDict(response)
        sendJSON(request, result)

    def _renderFailure(self, request, failure):
        sendJSONError(request, failure.value)

    def makeCall(self, request):
        try:
            args = convertArgs(request.args, self.method.argumentTypes)
            deferred = self.method(*args)
            if deferred is None:
                sendJSON(request, {'message': 'One way call made'})
                return
            deferred.addCallbacks(functools.partial(self._renderResponse, request), functools.partial(self._renderFailure, request))
        except Exception as e:
            import traceback
            traceback.print_exc()
            sendJSONError(request, e)

        return


class CallMailboxResource(TwoWayCallResource):

    def __init__(self, mailbox, methodName, filterFn = None):
        TwoWayCallResource.__init__(self, getattr(mailbox, methodName), filterFn)

    def render_GET(self, request):
        self.makeCall(request)
        return server.NOT_DONE_YET


def makeCallMailboxResource(*args, **kwargs):
    try:
        return CallMailboxResource(*args, **kwargs)
    except Exception as e:
        return ErrorPage(e)


import BigWorld

class CallEntityResource(TwoWayCallResource):

    def __init__(self, entityType, entityKey, methodName, addToKeepAliveCache = False, filterFn = None):
        TwoWayCallResource.__init__(self, filterFn=filterFn)
        self.entityType = entityType
        self.entityKey = entityKey
        self.methodName = methodName
        self.addToKeepAliveCache = addToKeepAliveCache

    def onMailbox(self, request, mailbox):
        if isinstance(mailbox, bool):
            sendJSONError(request, BWTwoWay.BWNoSuchEntityError('Not online'))
            return
        if self.addToKeepAliveCache:
            KeepAliveMailboxes.add(self.entityType, self.entityKey, mailbox)
        try:
            self.method = getattr(mailbox, self.methodName)
        except AttributeError as e:
            sendJSONError(request, BWTwoWay.BWNoSuchEntityError("Entity has no method '%s'" % self.methodName))
            return

        self.makeCall(request)

    def render_GET(self, request):
        self.lookUpFn(self.entityType, self.entityKey, functools.partial(self.onMailbox, request))
        return server.NOT_DONE_YET


def makeCallEntityResource(*args, **kwargs):
    try:
        return CallEntityResource(*args, **kwargs)
    except Exception as e:
        return ErrorPage(e)


class CallEntityResourceByName(CallEntityResource):
    lookUpFn = BigWorld.lookUpBaseByName

    def __init__(self, entityType, entityName, methodName):
        CallEntityResource.__init__(self, entityType, entityName, methodName)


def makeCallEntityResourceByName(*args, **kwargs):
    try:
        return CallEntityResourceByName(*args, **kwargs)
    except Exception as e:
        return ErrorPage(e)


class CallEntityResourceByID(CallEntityResource):
    lookUpFn = BigWorld.lookUpBaseByDBID

    def __init__(self, entityType, entityID, methodName, addToKeepAliveCache = False, filterFn = None):
        CallEntityResource.__init__(self, entityType, int(entityID), methodName, addToKeepAliveCache=addToKeepAliveCache, filterFn=filterFn)


def makeCallEntityResourceByID(*args, **kwargs):
    try:
        return CallEntityResourceByID(*args, **kwargs)
    except Exception as e:
        return ErrorPage(e)