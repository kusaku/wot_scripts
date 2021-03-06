# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TechnicalMaintenanceMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class TechnicalMaintenanceMeta(AbstractWindowView):

    def getEquipment(self, id1, currency1, id2, currency2, id3, currency3, installSlotIndex):
        self._printOverrideError('getEquipment')

    def repair(self):
        self._printOverrideError('repair')

    def setRefillSettings(self, vehicleCompact, repair, shells, equipment):
        self._printOverrideError('setRefillSettings')

    def showModuleInfo(self, moduleId):
        self._printOverrideError('showModuleInfo')

    def fillVehicle(self, needRepair, needAmmo, needEquipment, isPopulate, isUnload, isOrderChanged, shells, equipment):
        self._printOverrideError('fillVehicle')

    def updateEquipmentCurrency(self, equipmentIndex, currency):
        self._printOverrideError('updateEquipmentCurrency')

    def as_setDataS(self, data):
        """
        :param data: Represented by MaintenanceVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_setEquipmentS(self, installed, setup, modules):
        """
        :param installed: Represented by Array (AS)
        :param setup: Represented by Array (AS)
        :param modules: Represented by Array.<ModuleVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setEquipment(installed, setup, modules)

    def as_setCreditsS(self, credits):
        if self._isDAAPIInited():
            return self.flashObject.as_setCredits(credits)

    def as_setGoldS(self, gold):
        if self._isDAAPIInited():
            return self.flashObject.as_setGold(gold)

    def as_resetEquipmentS(self, equipmentCD):
        if self._isDAAPIInited():
            return self.flashObject.as_resetEquipment(equipmentCD)