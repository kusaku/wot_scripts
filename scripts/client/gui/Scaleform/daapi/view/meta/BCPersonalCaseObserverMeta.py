# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCPersonalCaseObserverMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class BCPersonalCaseObserverMeta(BaseDAAPIComponent):

    def onSkillClick(self, skillId):
        self._printOverrideError('onSkillClick')