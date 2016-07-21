# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/WrapperViewMeta.py
from gui.Scaleform.framework.entities.View import View

class WrapperViewMeta(View):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends View
    null
    """

    def onWindowClose(self):
        """
        :return :
        """
        self._printOverrideError('onWindowClose')

    def as_showWaitingS(self, msg, props):
        """
        :param msg:
        :param props:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_showWaiting(msg, props)

    def as_hideWaitingS(self):
        """
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_hideWaiting()