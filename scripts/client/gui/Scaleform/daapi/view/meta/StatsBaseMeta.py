# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/StatsBaseMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class StatsBaseMeta(BaseDAAPIComponent):

    def acceptSquad(self, uid):
        self._printOverrideError('acceptSquad')

    def addToSquad(self, uid):
        self._printOverrideError('addToSquad')

    def as_setIsIntaractiveS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setIsIntaractive(value)