# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanProfileGlobalMapPromoViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ClanProfileGlobalMapPromoViewMeta(BaseDAAPIComponent):

    def showInfo(self):
        self._printOverrideError('showInfo')

    def showMap(self):
        self._printOverrideError('showMap')

    def as_setDataS(self, data):
        """
        :param data: Represented by ClanProfileGlobalMapPromoVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)