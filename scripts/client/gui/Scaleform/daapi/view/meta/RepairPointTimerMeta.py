# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RepairPointTimerMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class RepairPointTimerMeta(BaseDAAPIComponent):

    def as_setStateS(self, state):
        if self._isDAAPIInited():
            return self.flashObject.as_setState(state)

    def as_setTimeInSecondsS(self, seconds):
        if self._isDAAPIInited():
            return self.flashObject.as_setTimeInSeconds(seconds)

    def as_setTimeStringS(self, timeStr):
        if self._isDAAPIInited():
            return self.flashObject.as_setTimeString(timeStr)

    def as_useActionScriptTimerS(self, isASTimer):
        if self._isDAAPIInited():
            return self.flashObject.as_useActionScriptTimer(isASTimer)

    def as_hideS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide()