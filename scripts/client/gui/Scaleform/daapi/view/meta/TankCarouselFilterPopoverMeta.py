# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TankCarouselFilterPopoverMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.popover.SmartPopOverView import SmartPopOverView

class TankCarouselFilterPopoverMeta(SmartPopOverView):

    def changeFilter(self, groupId, itemId):
        self._printOverrideError('changeFilter')

    def changeSearchNameVehicle(self, inputText):
        self._printOverrideError('changeSearchNameVehicle')

    def switchCarouselType(self, selected):
        self._printOverrideError('switchCarouselType')

    def as_setInitDataS(self, data):
        """
        :param data: Represented by FilterCarouseInitVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)

    def as_setStateS(self, data):
        """
        :param data: Represented by FiltersStateVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setState(data)

    def as_showCounterS(self, countText):
        if self._isDAAPIInited():
            return self.flashObject.as_showCounter(countText)