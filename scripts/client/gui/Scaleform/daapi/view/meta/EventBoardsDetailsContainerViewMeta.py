# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventBoardsDetailsContainerViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class EventBoardsDetailsContainerViewMeta(View):

    def closeView(self):
        self._printOverrideError('closeView')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by EventBoardsDetailsContainerVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)