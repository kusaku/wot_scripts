# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/LoaderManagerMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class LoaderManagerMeta(BaseDAAPIComponent):

    def viewLoaded(self, alias, viewName, view):
        self._printOverrideError('viewLoaded')

    def viewLoadError(self, alias, viewName, text):
        self._printOverrideError('viewLoadError')

    def viewInitializationError(self, alias, viewName):
        self._printOverrideError('viewInitializationError')

    def viewLoadCanceled(self, alias, viewName):
        self._printOverrideError('viewLoadCanceled')

    def as_loadViewS(self, data):
        """
        :param data: Represented by LoadViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_loadView(data)

    def as_cancelLoadViewS(self, viewName):
        if self._isDAAPIInited():
            return self.flashObject.as_cancelLoadView(viewName)