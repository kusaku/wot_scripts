# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PlayersPanelMeta.py
from gui.Scaleform.daapi.view.battle.classic.base_stats import StatsBase

class PlayersPanelMeta(StatsBase):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends StatsBase
    """

    def tryToSetPanelModeByMouse(self, panelMode):
        self._printOverrideError('tryToSetPanelModeByMouse')

    def switchToOtherPlayer(self, vehicleID):
        self._printOverrideError('switchToOtherPlayer')

    def as_setPanelModeS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setPanelMode(value)