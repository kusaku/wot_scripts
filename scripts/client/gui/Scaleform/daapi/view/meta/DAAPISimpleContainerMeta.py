# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/DAAPISimpleContainerMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIModule import BaseDAAPIModule

class DAAPISimpleContainerMeta(BaseDAAPIModule):

    def as_populateS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_populate()

    def as_disposeS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_dispose()