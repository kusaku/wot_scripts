# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesWidgetMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class RankedBattlesWidgetMeta(BaseDAAPIComponent):

    def onWidgetClick(self):
        self._printOverrideError('onWidgetClick')

    def onAnimationFinished(self):
        self._printOverrideError('onAnimationFinished')

    def onSoundTrigger(self, triggerName):
        self._printOverrideError('onSoundTrigger')

    def as_setDataS(self, states):
        """
        :param states: Represented by Vector.<RankedBattlesWidgetVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(states)