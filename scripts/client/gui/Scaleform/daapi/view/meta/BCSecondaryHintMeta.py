# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCSecondaryHintMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCSecondaryHintMeta(BaseDAAPIComponent):

    def as_hideHintS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideHint()

    def as_showHintS(self, text):
        if self._isDAAPIInited():
            return self.flashObject.as_showHint(text)