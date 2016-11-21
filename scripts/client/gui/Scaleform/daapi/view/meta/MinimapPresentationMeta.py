# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MinimapPresentationMeta.py
from gui.Scaleform.daapi.view.meta.MinimapEntityMeta import MinimapEntityMeta

class MinimapPresentationMeta(MinimapEntityMeta):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends MinimapEntityMeta
    """

    def setMap(self, arenaID):
        self._printOverrideError('setMap')

    def setMinimapData(self, arenaID, playerTeam, size):
        self._printOverrideError('setMinimapData')

    def as_changeMapS(self, texture):
        if self._isDAAPIInited():
            return self.flashObject.as_changeMap(texture)

    def as_addPointS(self, x, y, type, color, id):
        if self._isDAAPIInited():
            return self.flashObject.as_addPoint(x, y, type, color, id)

    def as_clearS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_clear()