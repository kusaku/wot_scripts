# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RssNewsFeedMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class RssNewsFeedMeta(BaseDAAPIComponent):

    def openBrowser(self, linkToOpen):
        self._printOverrideError('openBrowser')

    def as_updateFeedS(self, feed):
        """
        :param feed: Represented by Vector.<RssItemVo> (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_updateFeed(feed)