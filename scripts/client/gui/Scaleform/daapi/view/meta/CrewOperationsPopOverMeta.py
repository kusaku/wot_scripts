# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CrewOperationsPopOverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class CrewOperationsPopOverMeta(SmartPopOverView):

    def invokeOperation(self, operationName):
        self._printOverrideError('invokeOperation')

    def as_updateS(self, data):
        """
        :param data: Represented by CrewOperationsInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)