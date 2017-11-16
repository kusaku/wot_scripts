# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PvEHalloweenQueueWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class PvEHalloweenQueueWindowMeta(AbstractWindowView):

    def cancel(self):
        self._printOverrideError('cancel')

    def as_setDataS(self, data):
        """
        :param data: Represented by WaitingQueueWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)