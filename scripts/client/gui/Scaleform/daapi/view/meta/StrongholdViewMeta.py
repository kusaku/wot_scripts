# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/StrongholdViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class StrongholdViewMeta(View):

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')

    def onFocusChange(self, hasFocus):
        self._printOverrideError('onFocusChange')

    def viewSize(self, width, height):
        self._printOverrideError('viewSize')

    def as_loadBrowserS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_loadBrowser()