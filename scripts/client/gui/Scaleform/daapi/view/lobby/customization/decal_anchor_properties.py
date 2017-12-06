# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/customization/decal_anchor_properties.py
from gui.Scaleform.daapi.view.lobby.customization.anchor_properties import ANCHOR_TYPE
from gui.Scaleform.daapi.view.lobby.customization.anchor_properties import AnchorDataVO
from gui.Scaleform.daapi.view.meta.CustomizationDecalAnchorPropertiesMeta import CustomizationDecalAnchorPropertiesMeta
from gui.Scaleform.locale.RES_ICONS import RES_ICONS

class DecalDataVO(AnchorDataVO):
    pass


class DecalAnchorProperties(CustomizationDecalAnchorPropertiesMeta):

    def _getAnchorType(self):
        return ANCHOR_TYPE.DECAL

    def _getData(self):
        itemData = self._getItemData()
        if itemData is None:
            itemData = {'intCD': 0,
             'icon': RES_ICONS.MAPS_ICONS_LIBRARY_TANKITEM_BUY_TANK_POPOVER_SMALL}
        return DecalDataVO(self._name, self._desc, self._isEmpty, itemData).asDict()