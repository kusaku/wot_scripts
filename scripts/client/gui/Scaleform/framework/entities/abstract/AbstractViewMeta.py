# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/AbstractViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class AbstractViewMeta(BaseDAAPIComponent):

    def onFocusIn(self, alias):
        self._printOverrideError('onFocusIn')

    def as_setupContextHintBuilderS(self, builderLnk, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setupContextHintBuilder(builderLnk, data)