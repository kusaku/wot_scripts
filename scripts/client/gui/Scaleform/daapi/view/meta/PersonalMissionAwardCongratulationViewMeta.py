# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PersonalMissionAwardCongratulationViewMeta.py
from gui.Scaleform.daapi.view.meta.PersonalMissionsAbstractInfoViewMeta import PersonalMissionsAbstractInfoViewMeta

class PersonalMissionAwardCongratulationViewMeta(PersonalMissionsAbstractInfoViewMeta):

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')