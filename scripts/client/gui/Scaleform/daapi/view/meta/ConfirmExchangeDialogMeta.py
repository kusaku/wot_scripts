# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ConfirmExchangeDialogMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class ConfirmExchangeDialogMeta(AbstractWindowView):

    def exchange(self, goldValue):
        self._printOverrideError('exchange')

    def as_updateS(self, data):
        """
        :param data: Represented by ConfirmExchangeDialogVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_update(data)