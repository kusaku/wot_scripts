# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FortDisconnectViewMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class FortDisconnectViewMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def as_setWarningTextsS(self, warningTxt, warningDescTxt):
        """
        :param warningTxt:
        :param warningDescTxt:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setWarningTexts(warningTxt, warningDescTxt)