# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCTooltipsWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class BCTooltipsWindowMeta(View):

    def animFinish(self):
        self._printOverrideError('animFinish')

    def as_setRotateTipVisibilityS(self, Visible):
        if self._isDAAPIInited():
            return self.flashObject.as_setRotateTipVisibility(Visible)

    def as_showHandlerS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_showHandler()

    def as_completeHandlerS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_completeHandler()

    def as_hideHandlerS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideHandler()