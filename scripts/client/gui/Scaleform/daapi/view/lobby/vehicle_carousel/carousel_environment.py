# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/vehicle_carousel/carousel_environment.py
import constants
from CurrentVehicle import g_currentVehicle
from PlayerEvents import g_playerEvents
from account_helpers.settings_core import settings_constants
from gui.Scaleform.daapi.view.lobby.vehicle_carousel.carousel_data_provider import CarouselDataProvider
from gui.Scaleform.daapi.view.lobby.vehicle_carousel.carousel_filter import CarouselFilter
from gui.Scaleform.daapi.view.meta.CarouselEnvironmentMeta import CarouselEnvironmentMeta
from gui.prb_control.ctrl_events import g_prbCtrlEvents
from gui.prb_control.entities.listener import IGlobalListener
from gui.shared.formatters import text_styles
from gui.shared.gui_items import GUI_ITEM_TYPE
from gui.shared.items_cache import CACHE_SYNC_REASON
from gui.shared.utils.functions import makeTooltip
from gui.shared.utils.requesters.ItemsRequester import REQ_CRITERIA
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore
from skeletons.gui.game_control import IRentalsController, IIGRController, IClanLockController
from skeletons.gui.shared import IItemsCache
_CAROUSEL_FILTERS = ('bonus', 'favorite', 'elite', 'premium')
if constants.IS_KOREA:
    _CAROUSEL_FILTERS += ('igr',)

class CarouselEnvironment(CarouselEnvironmentMeta, IGlobalListener):
    """ Base vehicle carousel for embedding in interfaces.
    
    Consists of the carousel itself and surrounding facilities (data provider, filters)
    """
    rentals = dependency.descriptor(IRentalsController)
    igrCtrl = dependency.descriptor(IIGRController)
    clanLock = dependency.descriptor(IClanLockController)
    settingsCore = dependency.descriptor(ISettingsCore)
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        super(CarouselEnvironment, self).__init__()
        self._usedFilters = _CAROUSEL_FILTERS
        self._carouselDPConfig = {'carouselFilter': None,
         'itemsCache': None,
         'currentVehicle': None}
        self._carouselDPCls = CarouselDataProvider
        self._carouselFilterCls = CarouselFilter
        self._carouselDP = None
        self._currentVehicle = None
        return

    def onPlayerStateChanged(self, entity, roster, accountInfo):
        if accountInfo.isCurrentPlayer():
            self.updateAviability()

    def onUnitPlayerStateChanged(self, pInfo):
        if pInfo.isCurrentPlayer():
            self.updateAviability()

    def onPrbEntitySwitched(self):
        self.updateAviability()

    def onEnqueued(self, queueType, *args):
        self.updateAviability()

    def onDequeued(self, queueType, *args):
        self.updateAviability()

    @property
    def filter(self):
        if self._carouselDP is not None:
            return self._carouselDP.filter
        else:
            return

    def getTotalVehiclesCount(self):
        return self._carouselDP.getTotalVehiclesCount()

    def getCurrentVehiclesCount(self):
        return self._carouselDP.getCurrentVehiclesCount()

    def hasRentedVehicles(self):
        return self._carouselDP.hasRentedVehicles()

    def hasEventVehicles(self):
        return self._carouselDP.hasEventVehicles()

    def resetFilters(self):
        self.filter.reset()
        self.applyFilter()

    def applyFilter(self):
        self._carouselDP.applyFilter()
        if not self.filter.isDefault():
            drawAttention = self._carouselDP.getCurrentVehiclesCount() == 0
            self.as_showCounterS(self.formatCountVehicles(), drawAttention)
        else:
            self.as_hideCounterS()

    def formatCountVehicles(self):
        return self._formatCountString(self._carouselDP.getCurrentVehiclesCount(), self._carouselDP.getTotalVehiclesCount())

    def blinkCounter(self):
        self.as_blinkCounterS()

    def selectVehicle(self, idx):
        """ This method is called from flash when user clicks on carousel item.
        """
        self._carouselDP.selectVehicle(idx)

    def updateVehicles(self, vehicles = None, filterCriteria = None):
        self._carouselDP.updateVehicles(vehicles, filterCriteria)
        self.applyFilter()

    def updateAviability(self):
        state = self._currentVehicle.getViewState()
        self.as_setEnabledS(not state.isLocked())

    def _populate(self):
        super(CarouselEnvironment, self)._populate()
        self._currentVehicle = g_currentVehicle
        self.rentals.onRentChangeNotify += self.__updateRent
        self.igrCtrl.onIgrTypeChanged += self.__updateIgrType
        self.clanLock.onClanLockUpdate += self.__updateClanLocks
        self.itemsCache.onSyncCompleted += self.__onCacheResync
        self._currentVehicle.onChanged += self.__onCurrentVehicleChanged
        self.settingsCore.onSettingsChanged += self._onCarouselSettingsChange
        g_playerEvents.onVehicleBecomeElite += self.__onVehicleBecomeElite
        g_prbCtrlEvents.onVehicleClientStateChanged += self.__onVehicleClientStateChanged
        self.startGlobalListening()
        self._carouselDPConfig.update({'carouselFilter': self._carouselFilterCls(),
         'itemsCache': self.itemsCache,
         'currentVehicle': self._currentVehicle})
        self._carouselDP = self._carouselDPCls(**self._carouselDPConfig)
        setting = self.settingsCore.options.getSetting(settings_constants.GAME.VEHICLE_CAROUSEL_STATS)
        self._carouselDP.setShowStats(setting.get())
        self._carouselDP.setEnvironment(self.app)
        self._carouselDP.setFlashObject(self.as_getDataProviderS())
        self._carouselDP.buildList()
        self.applyFilter()
        self.updateAviability()
        self.as_setInitDataS({'counterCloseTooltip': makeTooltip('#tooltips:tanksFilter/counter/close/header', '#tooltips:tanksFilter/counter/close/body')})

    def _dispose(self):
        self.rentals.onRentChangeNotify -= self.__updateRent
        self.igrCtrl.onIgrTypeChanged -= self.__updateIgrType
        self.clanLock.onClanLockUpdate -= self.__updateClanLocks
        self.itemsCache.onSyncCompleted -= self.__onCacheResync
        self._currentVehicle.onChanged -= self.__onCurrentVehicleChanged
        self.settingsCore.onSettingsChanged -= self._onCarouselSettingsChange
        g_playerEvents.onVehicleBecomeElite -= self.__onVehicleBecomeElite
        g_prbCtrlEvents.onVehicleClientStateChanged -= self.__onVehicleClientStateChanged
        self.stopGlobalListening()
        self._currentVehicle = None
        self._carouselDP.fini()
        self._carouselDP = None
        self._carouselDPConfig.clear()
        super(CarouselEnvironment, self)._dispose()
        return

    def _onCarouselSettingsChange(self, diff):
        if settings_constants.GAME.VEHICLE_CAROUSEL_STATS in diff:
            setting = self.settingsCore.options.getSetting(settings_constants.GAME.VEHICLE_CAROUSEL_STATS)
            self._carouselDP.setShowStats(setting.get())
            self._carouselDP.updateVehicles()

    @staticmethod
    def _formatCountString(currentVehiclesCount, totalVehiclesCount):
        style = text_styles.error if currentVehiclesCount == 0 else text_styles.stats
        return '{} / {}'.format(style(currentVehiclesCount), text_styles.main(totalVehiclesCount))

    def __updateRent(self, vehicles):
        self.updateVehicles(vehicles)

    def __updateIgrType(self, roomType, xpFactor):
        self.updateVehicles(filterCriteria=REQ_CRITERIA.VEHICLE.IS_PREMIUM_IGR)

    def __updateClanLocks(self, vehicles, isFull):
        if isFull:
            self.updateVehicles()
        else:
            self.updateVehicles(vehicles)

    def __onCacheResync(self, reason, diff):
        if reason in (CACHE_SYNC_REASON.SHOP_RESYNC, CACHE_SYNC_REASON.DOSSIER_RESYNC):
            self.updateVehicles()
            self.updateAviability()
            return
        if reason in (CACHE_SYNC_REASON.STATS_RESYNC, CACHE_SYNC_REASON.INVENTORY_RESYNC, CACHE_SYNC_REASON.CLIENT_UPDATE):
            self.updateAviability()
        if GUI_ITEM_TYPE.VEHICLE in diff:
            self.updateVehicles(diff.get(GUI_ITEM_TYPE.VEHICLE))

    def __onCurrentVehicleChanged(self):
        self.updateAviability()

    def __onVehicleBecomeElite(self, *vehicles):
        self.updateVehicles(vehicles)

    def __onVehicleClientStateChanged(self, vehicles):
        self.updateVehicles(vehicles)