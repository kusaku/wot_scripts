# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanProfileTableStatisticsViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ClanProfileTableStatisticsViewMeta(BaseDAAPIComponent):

    def as_setDataS(self, data):
        """
        :param data: Represented by ClanProfileTableStatisticsDataVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setAdditionalTextS(self, visible, text):
        if self._isDAAPIInited():
            return self.flashObject.as_setAdditionalText(visible, text)

    def as_getDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getDP()