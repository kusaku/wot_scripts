# Embedded file name: scripts/client/skeletons/gui/shared/__init__.py
from Event import Event
from skeletons.gui.shared.utils import IItemsRequester, requesters

class IItemsCache(requesters.IRequester):
    onSyncStarted = None
    onSyncCompleted = None

    @property
    def waitForSync(self):
        raise NotImplementedError

    @property
    def items(self):
        raise NotImplementedError

    def init(self):
        raise NotImplementedError

    def fini(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def update(self, updateReason, diff = None, callback = None):
        raise NotImplementedError