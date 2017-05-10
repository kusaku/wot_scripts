# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/TickerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class TickerMeta(BaseDAAPIComponent):

    def showBrowser(self, entryID):
        self._printOverrideError('showBrowser')

    def as_setItemsS(self, items):
        """
        :param items: Represented by Vector.<RSSEntryVO> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setItems(items)