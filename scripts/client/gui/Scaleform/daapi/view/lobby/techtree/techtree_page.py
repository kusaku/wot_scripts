# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/techtree/techtree_page.py
import GUI
import Keys
import nations
from account_helpers.settings_core.settings_constants import TUTORIAL
from constants import IS_DEVELOPMENT
from debug_utils import LOG_DEBUG, LOG_ERROR
from gui import g_guiResetters
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.lobby.techtree import dumpers
from gui.Scaleform.daapi.view.lobby.techtree.data import NationTreeData
from gui.Scaleform.daapi.view.lobby.techtree.settings import SelectedNation
from gui.Scaleform.daapi.view.lobby.techtree.techtree_dp import g_techTreeDP
from gui.Scaleform.daapi.view.meta.TechTreeMeta import TechTreeMeta
from gui.shared import events, EVENT_BUS_SCOPE
from gui.shared.gui_items.items_actions import factory as ItemsActionsFactory
from gui.sounds.ambients import LobbySubViewEnv
_HEIGHT_LESS_THAN_SPECIFIED_TO_OVERRIDE = 768
_HEIGHT_LESS_THAN_SPECIFIED_OVERRIDE_TAG = 'height_less_768'

class TechTree(TechTreeMeta):
    __sound_env__ = LobbySubViewEnv

    def __init__(self, ctx = None):
        super(TechTree, self).__init__(NationTreeData(dumpers.NationObjDumper()))
        self._resolveLoadCtx(ctx=ctx)

    def __del__(self):
        LOG_DEBUG('TechTree deleted')

    def redraw(self):
        self.as_refreshNationTreeDataS(SelectedNation.getName())

    def requestNationTreeData(self):
        """
        Overridden method of the class _Py_ScriptHandler.requestNationTreeData.
        """
        self.as_setAvailableNationsS(g_techTreeDP.getAvailableNations())
        self.as_setSelectedNationS(SelectedNation.getName())
        return True

    def getNationTreeData(self, nationName):
        """
        Overridden method of the class _Py_ScriptHandler.getNationTreeData.
        """
        if nationName not in nations.INDICES:
            LOG_ERROR('Nation not found', nationName)
            return {}
        nationIdx = nations.INDICES[nationName]
        SelectedNation.select(nationIdx)
        self._data.load(nationIdx, override=self._getOverride())
        return self._data.dump()

    def request4Unlock(self, unlockCD, vehCD, unlockIdx, xpCost):
        """
        Overridden method of the class ResearchViewMeta.request4Unlock.
        """
        ItemsActionsFactory.doAction(ItemsActionsFactory.UNLOCK_ITEM, int(unlockCD), int(vehCD), int(unlockIdx), int(xpCost))

    def request4Buy(self, itemCD):
        """
        Overridden method of the class ResearchViewMeta.request4Buy
        """
        ItemsActionsFactory.doAction(ItemsActionsFactory.BUY_VEHICLE, int(itemCD))

    def request4VehCompare(self, vehCD):
        """
        :param vehCD: float
        """
        self.cmpBasket.addVehicle(int(vehCD))

    def request4Restore(self, itemCD):
        ItemsActionsFactory.doAction(ItemsActionsFactory.BUY_VEHICLE, int(itemCD))

    def goToNextVehicle(self, vehCD):
        exitEvent = events.LoadViewEvent(VIEW_ALIAS.LOBBY_TECHTREE, ctx={'nation': SelectedNation.getName()})
        loadEvent = events.LoadViewEvent(VIEW_ALIAS.LOBBY_RESEARCH, ctx={'rootCD': vehCD,
         'exit': exitEvent})
        self.fireEvent(loadEvent, scope=EVENT_BUS_SCOPE.LOBBY)

    def onCloseTechTree(self):
        if self._canBeClosed:
            self.fireEvent(events.LoadViewEvent(VIEW_ALIAS.LOBBY_HANGAR), scope=EVENT_BUS_SCOPE.LOBBY)

    def invalidateVehLocks(self, locks):
        """
        Overridden method of the class ResearchView.invalidateVehLocks.
        """
        if self._data.invalidateLocks(locks):
            self.redraw()

    def invalidateVTypeXP(self, xps):
        """
        Overridden method of the class ResearchView.invalidateVTypeXP.
        Experience cost of some vehicles may changes if xps of vehicles has been updated, @see WOTD-12753.
        """
        super(TechTree, self).invalidateVTypeXP(xps)
        result = self._data.invalidateXpCosts()
        if result:
            self.as_setUnlockPropsS(result)

    def invalidateWalletStatus(self, status):
        self.invalidateFreeXP()
        self.invalidateGold()

    def invalidateRent(self, vehicles):
        pass

    def invalidateRestore(self, vehicles):
        if self._data.invalidateRestore(vehicles):
            self.redraw()

    def _resolveLoadCtx(self, ctx = None):
        nation = ctx['nation'] if ctx is not None and 'nation' in ctx else None
        if nation is not None and nation in nations.INDICES:
            nationIdx = nations.INDICES[nation]
            SelectedNation.select(nationIdx)
        else:
            SelectedNation.byDefault()
        return

    def _getOverride(self):
        _, height = GUI.screenResolution()
        override = ''
        if height < _HEIGHT_LESS_THAN_SPECIFIED_TO_OVERRIDE or self.app.varsManager.isShowTicker() and height == _HEIGHT_LESS_THAN_SPECIFIED_TO_OVERRIDE:
            override = _HEIGHT_LESS_THAN_SPECIFIED_OVERRIDE_TAG
        return override

    def _populate(self):
        super(TechTree, self)._populate()
        g_guiResetters.add(self.__onUpdateStage)
        if IS_DEVELOPMENT:
            from gui import InputHandler
            InputHandler.g_instance.onKeyUp += self.__handleReloadData
        self.setupContextHints(TUTORIAL.RESEARCH_TREE)
        self._populateAfter()

    def _populateAfter(self):
        pass

    def _dispose(self):
        g_guiResetters.discard(self.__onUpdateStage)
        if IS_DEVELOPMENT:
            from gui import InputHandler
            InputHandler.g_instance.onKeyUp -= self.__handleReloadData
        super(TechTree, self)._dispose()
        self._disposeAfter()

    def _disposeAfter(self):
        pass

    def __onUpdateStage(self):
        g_techTreeDP.setOverride(self._getOverride())
        if g_techTreeDP.load():
            self.redraw()

    def __handleReloadData(self, event):
        """
        Redraw nation tree.
        """
        if event.key is Keys.KEY_R:
            g_techTreeDP.load(isReload=True)
            self.redraw()