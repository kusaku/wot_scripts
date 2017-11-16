# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PersonalMissionDetailsContainerViewMeta.py
from gui.Scaleform.daapi.view.meta.BaseMissionDetailsContainerViewMeta import BaseMissionDetailsContainerViewMeta

class PersonalMissionDetailsContainerViewMeta(BaseMissionDetailsContainerViewMeta):

    def useSheet(self, eventID):
        self._printOverrideError('useSheet')

    def startMission(self, eventID):
        self._printOverrideError('startMission')

    def retryMission(self, eventID):
        self._printOverrideError('retryMission')

    def declineMission(self, eventID):
        self._printOverrideError('declineMission')

    def obtainAward(self, eventID):
        self._printOverrideError('obtainAward')