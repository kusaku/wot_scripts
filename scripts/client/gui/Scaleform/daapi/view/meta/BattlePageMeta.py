# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BattlePageMeta.py
from gui.Scaleform.framework.entities.View import View

class BattlePageMeta(View):

    def as_checkDAAPIS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_checkDAAPI()

    def as_setPostmortemTipsVisibleS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setPostmortemTipsVisible(value)

    def as_setComponentsVisibilityS(self, visible, hidden):
        """
        :param visible: Represented by Vector.<String> (AS)
        :param hidden: Represented by Vector.<String> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setComponentsVisibility(visible, hidden)

    def as_isComponentVisibleS(self, componentKey):
        if self._isDAAPIInited():
            return self.flashObject.as_isComponentVisible(componentKey)

    def as_getComponentsVisibilityS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getComponentsVisibility()

    def as_toggleCtrlPressFlagS(self, isCtrlPressed):
        if self._isDAAPIInited():
            return self.flashObject.as_toggleCtrlPressFlag(isCtrlPressed)

    def as_onBattleLoadCompletedS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_onBattleLoadCompleted()