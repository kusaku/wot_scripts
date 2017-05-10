# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/BrowserWindow.py
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.meta.BrowserWindowMeta import BrowserWindowMeta
from gui.Scaleform.locale.WAITING import WAITING
from gui.shared import event_bus_handlers, events, EVENT_BUS_SCOPE

class BrowserWindow(BrowserWindowMeta):
    __metaclass__ = event_bus_handlers.EventBusListener

    def __init__(self, ctx = None):
        super(BrowserWindow, self).__init__()
        self.__size = ctx.get('size')
        self.__browserID = ctx.get('browserID')
        self.__customTitle = ctx.get('title')
        self.__showActionBtn = ctx.get('showActionBtn', True)
        self.__showWaiting = ctx.get('showWaiting', False)
        self.__showCloseBtn = ctx.get('showCloseBtn', False)
        self.__isSolidBorder = ctx.get('isSolidBorder', False)
        self.__alias = ctx.get('alias', '')
        self.__handlers = ctx.get('handlers', None)
        return

    def _onRegisterFlashComponent(self, viewPy, alias):
        super(BrowserWindow, self)._onRegisterFlashComponent(viewPy, alias)
        if alias == VIEW_ALIAS.BROWSER:
            viewPy.init(self.__browserID, self.__handlers, self.__alias)

    def onWindowClose(self):
        self.destroy()

    def _populate(self):
        super(BrowserWindow, self)._populate()
        self.as_configureS(self.__customTitle, self.__showActionBtn, self.__showCloseBtn, self.__isSolidBorder)
        self.as_setSizeS(*self.__size)
        if self.__showWaiting:
            self.as_showWaitingS(WAITING.LOADCONTENT, {})

    @event_bus_handlers.eventBusHandler(events.HideWindowEvent.HIDE_BROWSER_WINDOW, EVENT_BUS_SCOPE.LOBBY)
    def __handleBrowserClose(self, event):
        if event.ctx.get('browserID') == self.__browserID:
            self.destroy()