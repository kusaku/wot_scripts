# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ClanProfileBaseViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ClanProfileBaseViewMeta(BaseDAAPIComponent):

    def onHeaderButtonClick(self, actionId):
        self._printOverrideError('onHeaderButtonClick')

    def viewSize(self, width, height):
        self._printOverrideError('viewSize')

    def as_setClanInfoS(self, data):
        """
        :param data: Represented by ClanBaseInfoVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setClanInfo(data)

    def as_setHeaderStateS(self, data):
        """
        :param data: Represented by ClanProfileHeaderStateVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderState(data)

    def as_setClanEmblemS(self, source):
        if self._isDAAPIInited():
            return self.flashObject.as_setClanEmblem(source)

    def as_setDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(value)

    def as_showWaitingS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_showWaiting(value)

    def as_showDummyS(self, data):
        """
        :param data: Represented by DummyVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showDummy(data)

    def as_hideDummyS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hideDummy()

    def as_loadBrowserS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_loadBrowser()