# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/LoaderManagerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class LoaderManagerMeta(BaseDAAPIComponent):

    def viewLoaded(self, alias, name, view):
        self._printOverrideError('viewLoaded')

    def viewLoadError(self, alias, name, text):
        self._printOverrideError('viewLoadError')

    def viewInitializationError(self, alias, name):
        self._printOverrideError('viewInitializationError')

    def as_loadViewS(self, data):
        """
        :param data: Represented by LoadViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_loadView(data)