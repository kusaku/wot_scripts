# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PremiumWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.SimpleWindowMeta import SimpleWindowMeta

class PremiumWindowMeta(SimpleWindowMeta):

    def onRateClick(self, rateId):
        self._printOverrideError('onRateClick')

    def as_setHeaderS(self, prc, bonus1, bonus2):
        if self._isDAAPIInited():
            return self.flashObject.as_setHeader(prc, bonus1, bonus2)

    def as_setRatesS(self, data):
        """
        :param data: Represented by PremiumWindowRatesVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setRates(data)