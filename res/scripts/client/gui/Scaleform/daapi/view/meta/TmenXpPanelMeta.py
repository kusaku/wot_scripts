# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TmenXpPanelMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class TmenXpPanelMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def accelerateTmenXp(self, selected):
        """
        :param selected:
        :return :
        """
        self._printOverrideError('accelerateTmenXp')

    def as_setTankmenXpPanelS(self, visible, selected):
        """
        :param visible:
        :param selected:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTankmenXpPanel(visible, selected)