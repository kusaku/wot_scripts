# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/WGNCPollWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class WGNCPollWindowMeta(AbstractWindowView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends AbstractWindowView
    null
    """

    def onBtnClick(self):
        """
        :return :
        """
        self._printOverrideError('onBtnClick')

    def onLinkClick(self, actions):
        """
        :param actions:
        :return :
        """
        self._printOverrideError('onLinkClick')

    def as_setWindowTitleS(self, value):
        """
        :param value:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setWindowTitle(value)

    def as_setTextS(self, value):
        """
        :param value:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setText(value)

    def as_setButtonLblS(self, value):
        """
        :param value:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setButtonLbl(value)