# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCBattleResultMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class BCBattleResultMeta(View):

    def click(self):
        self._printOverrideError('click')

    def onAnimationAwardStart(self, id):
        self._printOverrideError('onAnimationAwardStart')

    def as_setDataS(self, data):
        """
        :param data: Represented by BCBattleViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)