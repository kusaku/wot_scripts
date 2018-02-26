# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BattleSessionListMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class BattleSessionListMeta(AbstractWindowView):

    def requestToJoinTeam(self, prbID, prbType):
        self._printOverrideError('requestToJoinTeam')

    def getClientID(self):
        self._printOverrideError('getClientID')

    def as_refreshListS(self, data):
        """
        :param data: Represented by DataProvider.<BSListRendererVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_refreshList(data)