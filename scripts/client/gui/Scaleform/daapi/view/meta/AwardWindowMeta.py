# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/AwardWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class AwardWindowMeta(AbstractWindowView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends AbstractWindowView
    null
    """

    def onOKClick(self):
        """
        :return :
        """
        self._printOverrideError('onOKClick')

    def onTakeNextClick(self):
        """
        :return :
        """
        self._printOverrideError('onTakeNextClick')

    def onCloseClick(self):
        """
        :return :
        """
        self._printOverrideError('onCloseClick')

    def as_setDataS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)