# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ChannelCarouselMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ChannelCarouselMeta(BaseDAAPIComponent):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseDAAPIComponent
    null
    """

    def channelOpenClick(self, itemID):
        """
        :param itemID:
        :return :
        """
        self._printOverrideError('channelOpenClick')

    def closeAll(self):
        """
        :return :
        """
        self._printOverrideError('closeAll')

    def channelCloseClick(self, itemID):
        """
        :param itemID:
        :return :
        """
        self._printOverrideError('channelCloseClick')

    def updateItemDataFocus(self, itemID, wndType, isFocusIn):
        """
        :param itemID:
        :param wndType:
        :param isFocusIn:
        :return :
        """
        self._printOverrideError('updateItemDataFocus')

    def updateItemDataOpened(self, itemID, wndType, isWindowOpened):
        """
        :param itemID:
        :param wndType:
        :param isWindowOpened:
        :return :
        """
        self._printOverrideError('updateItemDataOpened')

    def as_getDataProviderS(self):
        """
        :return Object:
        """
        if self._isDAAPIInited():
            return self.flashObject.as_getDataProvider()

    def as_getBattlesDataProviderS(self):
        """
        :return Object:
        """
        if self._isDAAPIInited():
            return self.flashObject.as_getBattlesDataProvider()