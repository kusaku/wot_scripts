# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/header/__init__.py
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ViewSettings, GroupedViewSettings, ViewTypes
from gui.Scaleform.framework import ScopeTemplates, ConditionalViewSettings
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.Scaleform.daapi.view.bootcamp.component_override import BootcampComponentOverride

def getContextMenuHandlers():
    return ()


def getViewSettings():
    from gui.Scaleform.daapi.view.lobby.header.AccountPopover import AccountPopover
    from gui.Scaleform.daapi.view.lobby.header.BattleTypeSelectPopover import BattleTypeSelectPopover
    from gui.Scaleform.daapi.view.lobby.header.SquadTypeSelectPopover import SquadTypeSelectPopover
    from gui.Scaleform.daapi.view.lobby.header.LobbyTicker import LobbyTicker
    from gui.Scaleform.daapi.view.lobby.header.LobbyHeader import LobbyHeader
    from gui.Scaleform.daapi.view.bootcamp.BCLobbyHeader import BCLobbyHeader
    return (GroupedViewSettings(VIEW_ALIAS.ACCOUNT_POPOVER, AccountPopover, 'accountPopover.swf', ViewTypes.WINDOW, 'accountPopover', VIEW_ALIAS.ACCOUNT_POPOVER, ScopeTemplates.DEFAULT_SCOPE),
     GroupedViewSettings(VIEW_ALIAS.BATTLE_TYPE_SELECT_POPOVER, BattleTypeSelectPopover, 'itemSelectorPopover.swf', ViewTypes.WINDOW, VIEW_ALIAS.BATTLE_TYPE_SELECT_POPOVER, VIEW_ALIAS.BATTLE_TYPE_SELECT_POPOVER, ScopeTemplates.DEFAULT_SCOPE),
     GroupedViewSettings(VIEW_ALIAS.SQUAD_TYPE_SELECT_POPOVER, SquadTypeSelectPopover, 'itemSelectorPopover.swf', ViewTypes.WINDOW, VIEW_ALIAS.SQUAD_TYPE_SELECT_POPOVER, VIEW_ALIAS.SQUAD_TYPE_SELECT_POPOVER, ScopeTemplates.DEFAULT_SCOPE),
     ConditionalViewSettings(VIEW_ALIAS.LOBBY_HEADER, BootcampComponentOverride(LobbyHeader, BCLobbyHeader), None, ViewTypes.COMPONENT, None, None, ScopeTemplates.DEFAULT_SCOPE),
     ViewSettings(VIEW_ALIAS.TICKER, LobbyTicker, None, ViewTypes.COMPONENT, None, ScopeTemplates.DEFAULT_SCOPE))


def getBusinessHandlers():
    return (HeaderPackageBusinessHandler(),)


class HeaderPackageBusinessHandler(PackageBusinessHandler):

    def __init__(self):
        listeners = ((VIEW_ALIAS.ACCOUNT_POPOVER, self.loadViewByCtxEvent), (VIEW_ALIAS.BATTLE_TYPE_SELECT_POPOVER, self.loadViewByCtxEvent), (VIEW_ALIAS.SQUAD_TYPE_SELECT_POPOVER, self.loadViewByCtxEvent))
        super(HeaderPackageBusinessHandler, self).__init__(listeners, APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)