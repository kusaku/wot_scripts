# Embedded file name: scripts/client/messenger/gui/Scaleform/meta/ContactNoteManageViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from messenger.gui.Scaleform.meta.BaseManageContactViewMeta import BaseManageContactViewMeta

class ContactNoteManageViewMeta(BaseManageContactViewMeta):

    def sendData(self, data):
        self._printOverrideError('sendData')

    def as_setUserPropsS(self, value):
        """
        :param value: Represented by ContactUserPropVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setUserProps(value)