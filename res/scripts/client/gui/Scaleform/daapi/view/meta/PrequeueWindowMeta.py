# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PrequeueWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class PrequeueWindowMeta(AbstractWindowView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends AbstractWindowView
    """

    def requestToEnqueue(self):
        self._printOverrideError('requestToEnqueue')

    def requestToLeave(self):
        self._printOverrideError('requestToLeave')

    def showFAQWindow(self):
        self._printOverrideError('showFAQWindow')

    def isEnqueueBtnEnabled(self):
        self._printOverrideError('isEnqueueBtnEnabled')

    def isLeaveBtnEnabled(self):
        self._printOverrideError('isLeaveBtnEnabled')

    def as_enableLeaveBtnS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_enableLeaveBtn(value)

    def as_enableEnqueueBtnS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_enableEnqueueBtn(value)