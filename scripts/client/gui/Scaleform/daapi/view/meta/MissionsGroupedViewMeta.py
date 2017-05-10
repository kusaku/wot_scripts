# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MissionsGroupedViewMeta.py
from gui.Scaleform.daapi.view.lobby.missions.missions_page import MissionView

class MissionsGroupedViewMeta(MissionView):

    def expand(self, id, value):
        self._printOverrideError('expand')

    def clickActionBtn(self, actionID):
        self._printOverrideError('clickActionBtn')

    def openTokenPopover(self, id):
        self._printOverrideError('openTokenPopover')