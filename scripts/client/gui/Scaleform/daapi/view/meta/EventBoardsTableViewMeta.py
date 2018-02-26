# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/EventBoardsTableViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class EventBoardsTableViewMeta(View):

    def closeView(self):
        self._printOverrideError('closeView')

    def setMyPlace(self):
        self._printOverrideError('setMyPlace')

    def participateStatusClick(self):
        self._printOverrideError('participateStatusClick')

    def playerClick(self, id):
        self._printOverrideError('playerClick')

    def showNextAward(self, visible):
        self._printOverrideError('showNextAward')

    def as_setHeaderDataS(self, data):
        """
        :param data: Represented by EventBoardsTableViewHeaderVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setHeaderData(data)

    def as_setStatusDataS(self, data):
        """
        :param data: Represented by EventBoardsTableViewStatusVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setStatusData(data)

    def as_setTableDataS(self, data):
        """
        :param data: Represented by EventBoardTableRendererContainerVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTableData(data)

    def as_setTableHeaderDataS(self, data):
        """
        :param data: Represented by EventBoardTableHeaderVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setTableHeaderData(data)

    def as_setBackgroundS(self, source):
        if self._isDAAPIInited():
            return self.flashObject.as_setBackground(source)

    def as_setScrollPosS(self, value, centered):
        if self._isDAAPIInited():
            return self.flashObject.as_setScrollPos(value, centered)

    def as_setMyPlaceVisibleS(self, visible):
        if self._isDAAPIInited():
            return self.flashObject.as_setMyPlaceVisible(visible)

    def as_setMyPlaceS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setMyPlace(value)

    def as_setMyPlaceTooltipS(self, tooltip):
        if self._isDAAPIInited():
            return self.flashObject.as_setMyPlaceTooltip(tooltip)

    def as_setStatusVisibleS(self, visible):
        if self._isDAAPIInited():
            return self.flashObject.as_setStatusVisible(visible)

    def as_setWaitingS(self, visible, message):
        if self._isDAAPIInited():
            return self.flashObject.as_setWaiting(visible, message)

    def as_setMaintenanceS(self, visible, message1, message2, buttonLabel):
        if self._isDAAPIInited():
            return self.flashObject.as_setMaintenance(visible, message1, message2, buttonLabel)

    def as_setAwardsStripesS(self, data):
        """
        :param data: Represented by EventBoardTableRendererContainerVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setAwardsStripes(data)

    def as_setEmptyDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setEmptyData(value)