# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCBattleResultMeta.py
from gui.Scaleform.framework.entities.View import View

class BCBattleResultMeta(View):

    def click(self):
        self._printOverrideError('click')

    def setReward(self, rewardIndex):
        self._printOverrideError('setReward')

    def onAnimationAwardStart(self, id):
        self._printOverrideError('onAnimationAwardStart')

    def as_setDataS(self, data):
        """
        :param data: Represented by BattleResultsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setBootcampDataS(self, data):
        """
        :param data: Represented by BCBattleViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setBootcampData(data)

    def as_resultTypeHandlerS(self, status, background):
        if self._isDAAPIInited():
            return self.flashObject.as_resultTypeHandler(status, background)