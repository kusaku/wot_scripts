# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/Fortifications2ViewMeta.py
from gui.Scaleform.framework.entities.View import View

class Fortifications2ViewMeta(View):

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')

    def onFocusChange(self, hasFocus):
        self._printOverrideError('onFocusChange')

    def viewSize(self, width, height):
        self._printOverrideError('viewSize')

    def as_loadBrowserS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_loadBrowser()