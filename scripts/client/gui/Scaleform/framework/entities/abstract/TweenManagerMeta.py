# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/TweenManagerMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class TweenManagerMeta(BaseDAAPIComponent):

    def createTween(self, tween):
        self._printOverrideError('createTween')

    def disposeTween(self, tween):
        self._printOverrideError('disposeTween')

    def disposeAll(self):
        self._printOverrideError('disposeAll')

    def as_setDataFromXmlS(self, data):
        """
        :param data: Represented by TweenConstraintsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setDataFromXml(data)