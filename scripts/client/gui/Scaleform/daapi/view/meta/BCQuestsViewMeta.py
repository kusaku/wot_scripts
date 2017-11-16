# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCQuestsViewMeta.py
from gui.Scaleform.framework.entities.View import View

class BCQuestsViewMeta(View):

    def onCloseClicked(self):
        self._printOverrideError('onCloseClicked')

    def as_setDataS(self, value):
        """
        :param value: Represented by BCQuestsViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(value)