# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/GameLoadingMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.DAAPISimpleContainerMeta import DAAPISimpleContainerMeta

class GameLoadingMeta(DAAPISimpleContainerMeta):

    def as_setLocaleS(self, locale):
        if self._isDAAPIInited():
            return self.flashObject.as_setLocale(locale)

    def as_setVersionS(self, version):
        if self._isDAAPIInited():
            return self.flashObject.as_setVersion(version)

    def as_setInfoS(self, info):
        if self._isDAAPIInited():
            return self.flashObject.as_setInfo(info)

    def as_setProgressS(self, progress):
        if self._isDAAPIInited():
            return self.flashObject.as_setProgress(progress)

    def as_updateStageS(self, width, height, scale):
        if self._isDAAPIInited():
            return self.flashObject.as_updateStage(width, height, scale)