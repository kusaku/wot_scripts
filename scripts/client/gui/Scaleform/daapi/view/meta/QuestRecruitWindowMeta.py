# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/QuestRecruitWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class QuestRecruitWindowMeta(AbstractWindowView):

    def onApply(self, data):
        self._printOverrideError('onApply')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by QuestRecruitWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)