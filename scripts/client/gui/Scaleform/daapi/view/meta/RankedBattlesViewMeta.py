# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesViewMeta.py
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class RankedBattlesViewMeta(WrapperViewMeta):

    def onCloseBtnClick(self):
        self._printOverrideError('onCloseBtnClick')

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')

    def onAwardClick(self, awardID):
        self._printOverrideError('onAwardClick')

    def onPlayBtnClick(self):
        self._printOverrideError('onPlayBtnClick')

    def as_setDataS(self, data):
        """
        :param data: Represented by RankedBattlesViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)