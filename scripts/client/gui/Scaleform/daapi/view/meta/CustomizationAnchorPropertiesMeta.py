# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationAnchorPropertiesMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class CustomizationAnchorPropertiesMeta(BaseDAAPIComponent):

    def applyData(self, areaId, slotId, regionId):
        self._printOverrideError('applyData')