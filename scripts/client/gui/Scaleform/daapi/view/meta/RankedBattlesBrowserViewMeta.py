# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesBrowserViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class RankedBattlesBrowserViewMeta(WrapperViewMeta):

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')

    def onCloseBtnClick(self):
        self._printOverrideError('onCloseBtnClick')

    def onFocusChange(self, hasFocus):
        self._printOverrideError('onFocusChange')

    def viewSize(self, width, height):
        self._printOverrideError('viewSize')

    def as_loadBrowserS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_loadBrowser()