# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RoleChangeMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class RoleChangeMeta(AbstractWindowView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends AbstractWindowView
    null
    """

    def onVehicleSelected(self, vehicleId):
        """
        :param vehicleId:
        :return :
        """
        self._printOverrideError('onVehicleSelected')

    def changeRole(self, role, vehicleId):
        """
        :param role:
        :param vehicleId:
        :return :
        """
        self._printOverrideError('changeRole')

    def as_setCommonDataS(self, data):
        """
        :param data:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setCommonData(data)

    def as_setRolesS(self, roles):
        """
        :param roles:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setRoles(roles)

    def as_setPriceS(self, priceString, enoughGold):
        """
        :param priceString:
        :param enoughGold:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setPrice(priceString, enoughGold)