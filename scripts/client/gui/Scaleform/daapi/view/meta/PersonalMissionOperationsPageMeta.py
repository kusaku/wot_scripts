# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PersonalMissionOperationsPageMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class PersonalMissionOperationsPageMeta(View):

    def closeView(self):
        self._printOverrideError('closeView')

    def showAwards(self):
        self._printOverrideError('showAwards')

    def showInfo(self):
        self._printOverrideError('showInfo')

    def onOperationClick(self, operationID):
        self._printOverrideError('onOperationClick')

    def as_setDataS(self, data):
        """
        :param data: Represented by OperationsPageVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)