# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/CustomizationFiltersPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class CustomizationFiltersPopoverMeta(SmartPopOverView):

    def changeGroup(self, itemId):
        self._printOverrideError('changeGroup')

    def setDefaultFilter(self):
        self._printOverrideError('setDefaultFilter')

    def setShowOnlyHistoric(self, value):
        self._printOverrideError('setShowOnlyHistoric')

    def setShowOnlyAcquired(self, value):
        self._printOverrideError('setShowOnlyAcquired')

    def onFilterChange(self, index, value):
        self._printOverrideError('onFilterChange')

    def as_setDataS(self, data):
        """
        :param data: Represented by FiltersPopoverVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_enableDefBtnS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_enableDefBtn(value)