# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/BCPersonalCaseMeta.py
from gui.Scaleform.daapi.view.lobby.PersonalCase import PersonalCase

class BCPersonalCaseMeta(PersonalCase):

    def onSkillClick(self, skillId):
        self._printOverrideError('onSkillClick')