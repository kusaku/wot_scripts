# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/PersonalMissionsAwardsViewMeta.py
from gui.Scaleform.framework.entities.View import View

class PersonalMissionsAwardsViewMeta(View):

    def showVehiclePreview(self):
        self._printOverrideError('showVehiclePreview')

    def changeOperation(self, operationID):
        self._printOverrideError('changeOperation')

    def closeView(self):
        self._printOverrideError('closeView')

    def showMissionByVehicleType(self, vehicleType):
        self._printOverrideError('showMissionByVehicleType')

    def buyMissionsByVehicleType(self, vehicleType):
        self._printOverrideError('buyMissionsByVehicleType')

    def as_setDataS(self, data):
        """
        :param data: Represented by PersonalMissionsAwardsViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setHeaderDataS(self, data):
        """
        :param data: Represented by OperationsHeaderVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderData(data)