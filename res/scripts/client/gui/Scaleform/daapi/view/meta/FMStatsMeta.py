# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FMStatsMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class FMStatsMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def as_setSubTypeS(self, value):
        """
        :param value:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setSubType(value)