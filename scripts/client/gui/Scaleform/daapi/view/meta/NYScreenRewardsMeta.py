# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYScreenRewardsMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class NYScreenRewardsMeta(View):

    def onClose(self):
        self._printOverrideError('onClose')

    def onRecruitClick(self, level):
        self._printOverrideError('onRecruitClick')

    def onDiscountApplyClick(self, level, vehicleLevel, discount):
        self._printOverrideError('onDiscountApplyClick')

    def as_initS(self, data):
        """
        :param data: Represented by NYScreenRewardsDataVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_init(data)