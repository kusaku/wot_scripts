# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/store/tabs/__init__.py
import constants
from gui import makeHtmlString
from gui.Scaleform.daapi.view.lobby.vehicle_compare.formatters import resolveStateTooltip
from gui.Scaleform.genConsts.STORE_CONSTANTS import STORE_CONSTANTS
from gui.Scaleform.genConsts.SLOT_HIGHLIGHT_TYPES import SLOT_HIGHLIGHT_TYPES
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.VEH_COMPARE import VEH_COMPARE
from gui.prb_control.settings import VEHICLE_LEVELS
from gui.shared.economics import getActionPrc
from gui.shared.formatters import text_styles, icons
from gui.shared.formatters.time_formatters import RentLeftFormatter, getTimeLeftInfo
from gui.shared.gui_items import GUI_ITEM_TYPE
from gui.shared.gui_items.Vehicle import VEHICLE_TYPES_ORDER
from gui.shared.money import ZERO_MONEY, Money
from gui.shared.utils import CLIP_ICON_PATH, HYDRAULIC_ICON_PATH, EXTRA_MODULE_INFO
from gui.shared.utils.requesters import REQ_CRITERIA
from helpers import i18n, time_utils, dependency
from helpers.i18n import makeString
from items import ITEM_TYPE_INDICES
from skeletons.gui.game_control import IVehicleComparisonBasket
from skeletons.gui.shared import IItemsCache
from gui.shared.gui_items.Vehicle import Vehicle

def _getBtnVehCompareData(vehicle):
    comparisonBasket = dependency.instance(IVehicleComparisonBasket)
    state, tooltip = resolveStateTooltip(comparisonBasket, vehicle, enabledTooltip=VEH_COMPARE.STORE_COMPAREVEHICLEBTN_TOOLTIPS_ADDTOCOMPARE, fullTooltip=VEH_COMPARE.STORE_COMPAREVEHICLEBTN_TOOLTIPS_DISABLED)
    return {'modeAvailable': comparisonBasket.isEnabled(),
     'btnEnabled': state,
     'btnTooltip': tooltip}


class StoreItemsTab(object):

    @dependency.replace_none_kwargs(itemsCache=IItemsCache)
    def __init__(self, nation, filtersData, actionsSelected, itemCD, itemsCache = None):
        """
        Base class for accordion tab in store component
        :param nation: <int> nation idx
        :param filtersData: <obj> filters data
        """
        self._nation = nation
        self._filterData = filtersData
        self._actionsSelected = actionsSelected
        self._itemCD = itemCD
        self._items = itemsCache.items
        self._scrollIdx = 0
        self._hasDiscounts = False

    def clear(self):
        """
        Clear tab attrs and fields
        """
        self._nation = None
        self._filterData = None
        self._items = None
        self._actionsSelected = False
        self._itemCD = None
        self._scrollIdx = 0
        self._hasDiscounts = False
        return

    def getScrollIdx(self):
        """
        Get index of the item that we should scroll to.
        Returns 0 if no scrolling is intended.
        :return:<int>
        """
        return self._scrollIdx

    def hasDiscounts(self):
        """
        Check whether there are some items with discounts among the items with
        applied filters.
        :return:<bool>
        """
        return self._hasDiscounts

    def buildItems(self, invVehicles):
        """
        Build items for StoreTableDataProvider
        :param invVehicles: <list(Vehicle,..)>
        :return: dataProviderValues: <[(item:<FittingItem>, extraModuleInfo:<str>, installedVehiclesCount:<int>),..]>
        """
        criteria = self._getRequestCriteria(invVehicles) | self._getDiscountCriteria()
        items = self._items.getItems(self._getItemTypeID(), criteria, self._nation)
        dataProviderValues = []
        for idx, item in enumerate(sorted(items.itervalues(), cmp=self._getComparator())):
            if self._itemCD and item.intCD == self._itemCD:
                self._scrollIdx = idx
            if self._isItemOnDiscount(item):
                self._hasDiscounts = True
            extraModuleInfo, installedVehiclesCount = self._getExtraParams(item, invVehicles)
            dataProviderValues.append((item, extraModuleInfo, installedVehiclesCount))

        return dataProviderValues

    def itemWrapper(self, packedItem):
        """
        Item wrapper for StoreTableDataProvider,
        prepare VO objects for flash
        :param packedItem:<tuple(item:<FittingItem>, extraModuleInfo:<str>, installedVehiclesCount:<int>)>
        :return: <obj> VO for flash
        """
        item, extraModuleInfo, installedVehiclesCount = packedItem
        statusMessage, disabled, statusImgSrc, isCritLvl = self.__getStatusInfo(item)
        stats = self._items.stats
        shop = self._items.shop
        price = self._getItemPrice(item)
        creditsActionPrc, goldActionPrc = self._getActionAllPercents(item)
        showActionGoldAndCredits = creditsActionPrc != 0 and goldActionPrc != 0 and creditsActionPrc != goldActionPrc
        return {'id': str(item.intCD),
         'name': self._getItemName(item),
         'desc': item.getShortInfo(),
         'inventoryId': self._getItemInventoryID(item),
         'inventoryCount': item.inventoryCount,
         'vehicleCount': installedVehiclesCount,
         'credits': stats.credits,
         'gold': stats.gold,
         'price': price,
         'currency': self._getCurrency(item),
         'level': item.level,
         'nation': item.nationID,
         'type': self._getItemTypeIcon(item),
         'disabled': disabled,
         'statusMessage': statusMessage,
         'isCritLvl': isCritLvl,
         'statusImgSrc': statusImgSrc,
         'removable': item.isRemovable,
         'itemTypeName': item.itemTypeName,
         'goldShellsForCredits': shop.isEnabledBuyingGoldShellsForCredits,
         'goldEqsForCredits': shop.isEnabledBuyingGoldEqsForCredits,
         'actionPriceData': self._getItemActionData(item),
         'moduleLabel': item.getGUIEmblemID(),
         EXTRA_MODULE_INFO: extraModuleInfo,
         'vehCompareData': _getBtnVehCompareData(item) if item.itemTypeID == GUI_ITEM_TYPE.VEHICLE else {},
         'highlightType': SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT,
         'showActionGoldAndCredits': showActionGoldAndCredits,
         'actionCreditsPercent': '-{}'.format(creditsActionPrc),
         'actionGoldPercent': '-{}'.format(goldActionPrc)}

    def _getItemTypeIcon(self, item):
        """
        Get item icon or itemTypeName frame
        :param item:<FittingItem>
        :return: <str>
        """
        return item.icon

    def _getItemInventoryID(self, item):
        """
        :param item:<FittingItem>
        :return:<int> inventory ID
        """
        return None

    def _getItemActionData(self, item):
        """
        Get data for store action
        :param item:<FittingItem>
        :return:<obj>
        """
        return None

    def _getItemName(self, item):
        """
        Get item name
        :param item:<FittingItem>
        :return:<str>
        """
        return item.longUserName

    def _getExtraParams(self, item, invVehicles):
        """
        Get extraModuleInfo and installed vehicles count
        :param item:<FittingItem>
        :param invVehicles:<[Vehicle,..]>
        :return: <tuple(extraModuleInfo<str>, installedVehiclesCount:<int>)>
        """
        return (None, 0)

    def _getStatusParams(self, item):
        """
        Get renderer disable state and its status
        :param item:<FittingItem>
        :return: <tuple(statusMessage<str>, disabled:<bool>)>
        """
        return ('', False)

    def _getStatusImg(self, item):
        """
        Get status image
        :param item: item to get status
        :return: string
        """
        return ''

    def _getItemPrice(self, item):
        """
        Get store item price
        :param item:<FittingItem>
        :return:<Money>
        """
        return ZERO_MONEY

    def _getItemDefaultPrice(self, item):
        """
        Get store item default price
        :param item:<FittingItem>
        :return:<Money>
        """
        return ZERO_MONEY

    def _getCurrency(self, item):
        """
        Get item price currency
        :param item:<FittingItem>
        :return:<str>
        """
        return self._getItemPrice(item).getCurrency()

    def _getComparator(self):
        """
        :return: <function> sort items function
        """
        return None

    def _getItemStatusLevel(self, item):
        """
        :param item:<FittingItem>
        :return: <str> status VEHICLE_STATE_LEVEL
        """
        raise NotImplementedError

    def _getItemTypeID(self):
        """
        Get itemTypeID or itemTypeIDs for ItemsRequester
        :return: tuple(itemTypeID:<int>,)
        """
        raise NotImplementedError

    def _getRequestCriteria(self, invVehicles):
        """
        Get request criteria for ItemsRequester from self._filterData
        :param invVehicles:<list(Vehicle,..)>
        :return: <RequestCriteria>
        """
        raise NotImplementedError

    def _getExtraCriteria(self, extra, requestCriteria, invVehicles):
        """
        Get additional request criteria for ItemsRequester from 'extra' field and adds it to base criteria
        :param extra: <list(extraField:<str>,..)>
        :param requestCriteria:<RequestCriteria>
        :param invVehicles:<list(Vehicle,..)>
        :return:<RequestCriteria>
        """
        raise NotImplementedError

    def _getDiscountCriteria(self):
        """
        Get additional request criteria from the discount field.
        :return: <RequestCriteria>
        """
        raise NotImplementedError

    def _isItemOnDiscount(self, item):
        """
        Determine whether item has discount or not.
        :param item:<FittingItem>
        :return: <Bool>
        """
        raise NotImplementedError

    @classmethod
    def getFilterInitData(cls):
        """
        Get filter init setting for AS, to create filters in tab,
        showExtra - flag to display extra fields (checkBoxes) in tab
        :return:<tuple(voClassName:<str>, showExtra:<bool>)>
        """
        raise NotImplementedError

    @classmethod
    def getTableType(cls):
        """
        Get table GUI type
        :return:<str>
        """
        raise NotImplementedError

    def __getStatusInfo(self, item):
        """
        Returns styled status message, image, critLevel flag
        :param item: item:<FittingItem>
        :return: tuple with values of styledStatus, disabled flag, statusImage icon, isCritLevel flag
        """
        isCritLvl = self._getItemStatusLevel(item) == Vehicle.VEHICLE_STATE_LEVEL.CRITICAL
        statusMessage, disabled = self._getStatusParams(item)
        if statusMessage:
            statusImgSrc = self._getStatusImg(item)
            styledStatus = text_styles.vehicleStatusCriticalText(statusMessage) if isCritLvl else text_styles.vehicleStatusInfoText(statusMessage)
        else:
            statusImgSrc = ''
            styledStatus = ''
        return (styledStatus,
         disabled,
         statusImgSrc,
         isCritLvl)

    def _getActionAllPercents(self, item):
        """
        Returns tuple with values of percent credits and golds discount
        :param item:
        :return: tuple
        """
        price = self._getItemPrice(item)
        defPrice = self._getItemDefaultPrice(item)
        creditsActionPrc = abs(getActionPrc(price.credits, defPrice.credits))
        goldActionPrc = abs(getActionPrc(price.gold, defPrice.gold))
        return (creditsActionPrc, goldActionPrc)


class StoreModuleTab(StoreItemsTab):

    @classmethod
    def getFilterInitData(cls):
        return (STORE_CONSTANTS.EXT_FIT_ITEMS_FILTERS_VO_CLASS, False)

    @classmethod
    def getTableType(cls):
        return STORE_CONSTANTS.MODULE

    def _getItemTypeID(self):
        return tuple(map(lambda x: ITEM_TYPE_INDICES[x], self._filterData['itemTypes']))

    def _getExtraParams(self, item, invVehicles):
        extraModuleInfo = None
        if item.itemTypeID == GUI_ITEM_TYPE.GUN and item.isClipGun():
            extraModuleInfo = CLIP_ICON_PATH
        elif item.itemTypeID == GUI_ITEM_TYPE.CHASSIS and item.isHydraulicChassis():
            extraModuleInfo = HYDRAULIC_ICON_PATH
        installedVehicles = item.getInstalledVehicles(invVehicles)
        return (extraModuleInfo, len(installedVehicles))

    def _getItemTypeIcon(self, item):
        return item.itemTypeName


class StoreVehicleTab(StoreItemsTab):

    @classmethod
    def getFilterInitData(cls):
        return (STORE_CONSTANTS.VEHICLES_FILTERS_VO_CLASS, True)

    @classmethod
    def getTableType(cls):
        return STORE_CONSTANTS.VEHICLE

    def itemWrapper(self, packedItem):
        item, _, _ = packedItem
        vo = super(StoreVehicleTab, self).itemWrapper(packedItem)
        vo.update({'tankType': item.type,
         'isPremium': item.isPremium,
         'isElite': item.isElite,
         'rentLeft': self.__getItemRentInfo(item),
         'restoreInfo': self.__getItemRestoreInfo(item),
         'canTradeIn': item.canTradeIn})
        return vo

    def _getItemTypeID(self):
        return GUI_ITEM_TYPE.VEHICLE

    def _getVehicleRiterias(self, selectedTypes, selectedLevels):
        requestCriteria = REQ_CRITERIA.EMPTY
        selectedVehiclesIds = []
        for idx, vehicleType in enumerate(VEHICLE_TYPES_ORDER):
            if selectedTypes[idx]:
                selectedVehiclesIds.append(vehicleType)

        if selectedVehiclesIds:
            requestCriteria |= REQ_CRITERIA.VEHICLE.CLASSES(selectedVehiclesIds)
        selectedLevelIds = []
        for level in VEHICLE_LEVELS:
            if selectedLevels[level - 1]:
                selectedLevelIds.append(level)

        if selectedLevelIds:
            requestCriteria |= REQ_CRITERIA.VEHICLE.LEVELS(selectedLevelIds)
        return requestCriteria

    def __getItemRestoreInfo(self, item):
        """
        Get formatted vehicle restore info
        :param item: <Vehicle>
        :return: <str>
        """
        if item.isRestorePossible():
            if constants.IS_CHINA and item.rentalIsActive:
                return text_styles.alert(MENU.VEHICLE_RESTORELEFT_DISABLEDBYRENT)
            if item.hasLimitedRestore():
                restoreLeftTime = item.restoreInfo.getRestoreTimeLeft()
                timeKey, formattedTime = getTimeLeftInfo(restoreLeftTime)
                msg = i18n.makeString('#menu:vehicle/restoreLeft/%s' % timeKey, time=formattedTime)
                if restoreLeftTime < time_utils.ONE_DAY:
                    return icons.alert() + text_styles.alert(msg)
                return text_styles.stats(msg)
            if item.hasRestoreCooldown():
                timeKey, formattedTime = getTimeLeftInfo(item.restoreInfo.getRestoreCooldownTimeLeft())
                msg = i18n.makeString('#menu:vehicle/restoreCooldownLeft/%s' % timeKey, time=formattedTime)
                return text_styles.stats(msg)
        return ''

    def __getItemRentInfo(self, item):
        """
        Get formatted vehicle rent info
        :param item: <Vehicle>
        :return:  <str>
        """
        if item.isRented:
            formatter = RentLeftFormatter(item.rentInfo, item.isPremiumIGR)
            return formatter.getRentLeftStr('#tooltips:vehicle/rentLeft/%s', formatter=lambda key, countType, count, _ = None: ''.join([makeString(key % countType), ': ', str(count)]))
        elif item.isRentable and item.isRentAvailable:
            minRentPricePackage = item.getRentPackage()
            priceText = ''
            discountText = ''
            if minRentPricePackage:
                minRentPriceValue = Money(*minRentPricePackage['rentPrice'])
                actionPrc = item.getRentPackageActionPrc(minRentPricePackage['days'])
                currency = minRentPriceValue.getCurrency()
                price = minRentPriceValue.get(currency)
                priceText = makeHtmlString('html_templates:lobby/quests/actions', currency, {'value': price})
                if actionPrc != 0:
                    discountText = makeString('#menu:shop/menu/vehicle/rent/discount', discount=text_styles.gold('{} %'.format(actionPrc)))
            rentText = makeString('#menu:shop/menu/vehicle/rent/available', price=priceText)
            return '{}  {}'.format(rentText, discountText)
        else:
            return ''


class StoreShellTab(StoreItemsTab):

    @classmethod
    def getTableType(cls):
        return STORE_CONSTANTS.SHELL

    @classmethod
    def getFilterInitData(cls):
        return (STORE_CONSTANTS.EXT_FIT_ITEMS_FILTERS_VO_CLASS, False)

    def _getItemTypeID(self):
        return GUI_ITEM_TYPE.SHELL


class StoreArtefactTab(StoreItemsTab):

    def _getExtraParams(self, item, invVehicles):
        return (None, len(item.getInstalledVehicles(invVehicles)))

    def _parseFilter(self, filtersList):
        fitsType = filtersList.pop(0)
        vehicleCD = filtersList.pop(0)
        extra = filtersList
        return {'vehicleCD': vehicleCD,
         'extra': extra,
         'fitsType': fitsType}

    @classmethod
    def getFilterInitData(cls):
        return (STORE_CONSTANTS.FIT_ITEMS_FILTERS_VO_CLASS, False)

    def _getItemName(self, item):
        return item.userName


class StoreOptionalDeviceTab(StoreArtefactTab):

    def itemWrapper(self, packedItem):
        vo = super(StoreArtefactTab, self).itemWrapper(packedItem)
        item = packedItem[0]
        if item.isDeluxe():
            vo['highlightType'] = SLOT_HIGHLIGHT_TYPES.EQUIPMENT_PLUS
        return vo

    @classmethod
    def getTableType(cls):
        return STORE_CONSTANTS.OPTIONAL_DEVICE

    def _getItemTypeID(self):
        return GUI_ITEM_TYPE.OPTIONALDEVICE

    def _isItemRemovable(self, item):
        return item.isRemovable


class StoreEquipmentTab(StoreArtefactTab):

    @classmethod
    def getTableType(cls):
        return STORE_CONSTANTS.EQUIPMENT

    def _getItemTypeID(self):
        return GUI_ITEM_TYPE.EQUIPMENT