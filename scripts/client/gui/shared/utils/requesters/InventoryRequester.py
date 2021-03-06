# Embedded file name: scripts/client/gui/shared/utils/requesters/InventoryRequester.py
import time
from collections import namedtuple, defaultdict
import BigWorld
from adisp import async
from constants import CustomizationInvData
from items import vehicles, tankmen, getTypeOfCompactDescr, parseIntCompactDescr
from debug_utils import LOG_DEBUG
from gui.shared.gui_items import GUI_ITEM_TYPE
from gui.shared.utils.requesters.abstract import AbstractSyncDataRequester
from skeletons.gui.shared.utils.requesters import IInventoryRequester

class InventoryRequester(AbstractSyncDataRequester, IInventoryRequester):
    VEH_DATA = namedtuple('VEH_DATA', ('compDescr', 'descriptor', 'invID', 'repair', 'crew', 'lock', 'settings', 'shells', 'shellsLayout', 'eqs', 'eqsLayout'))
    ITEM_DATA = namedtuple('ITEM_DATA', ('compDescr', 'descriptor', 'count'))
    TMAN_DATA = namedtuple('TMAN_DATA', ('compDescr', 'descriptor', 'vehicle', 'invID'))
    OUTFIT_DATA = namedtuple('OUTFIT_DATA', ('compDescr', 'isEnabled'))

    def __init__(self):
        super(InventoryRequester, self).__init__()
        self.__itemsCache = defaultdict(dict)
        self.__itemsPreviousCache = defaultdict(dict)
        self.__vehsCDsByID = {}
        self.__vehsIDsByCD = {}

    def clear(self):
        self.__itemsCache.clear()
        self.__itemsPreviousCache.clear()
        self.__vehsCDsByID.clear()
        self.__vehsIDsByCD.clear()
        super(InventoryRequester, self).clear()

    def invalidateItem(self, itemTypeID, invIdx):
        cache = self.__itemsCache[itemTypeID]
        if invIdx in cache:
            self.__itemsPreviousCache[itemTypeID][invIdx] = cache[invIdx]
            del cache[invIdx]
            return True
        return False

    def getItemsData(self, itemTypeID):
        invData = self.getCacheValue(itemTypeID, {})
        for invID in invData.get('compDescr', {}).iterkeys():
            self.__makeItem(itemTypeID, invID)

        return self.__itemsCache[itemTypeID]

    def getItemData(self, typeCompDescr):
        itemTypeID = getTypeOfCompactDescr(typeCompDescr)
        if itemTypeID == GUI_ITEM_TYPE.VEHICLE:
            return self.getVehicleData(self.__vehsIDsByCD.get(typeCompDescr, -1))
        return self.__makeSimpleItem(typeCompDescr)

    def getTankmanData(self, tmanInvID):
        return self.__makeTankman(tmanInvID)

    def getVehicleData(self, vehInvID):
        return self.__makeVehicle(vehInvID)

    def getOutfitData(self, intCD, season):
        """ Get an outfit data for the given vehicle intCD.
        
        :param intCD: int compact descr of a vehicle.
        :param season: season of outfit
        """
        return self.__makeOutfit(intCD, season)

    def getPreviousItem(self, itemTypeID, invDataIdx):
        return self.__itemsPreviousCache[itemTypeID].get(invDataIdx)

    def getItems(self, itemTypeIdx, dataIdx = None):
        """
        Returns inventory items data by given item type. If data index is
        not specified - returns dictionary of items data, otherwise -
        specific item data.
        
        @param itemTypeIdx: item type index from common.items.ITEM_TYPE_NAMES
        @param dataIdx:optional  item data index in cache. Used to get data only for
                                specific item. This index is different for each item type:
                                        - for vehicles and tankmen: inventory id
                                        - for the rest types: type compact descriptor (int)
        @return: dict of items data or specific item data
        """
        if itemTypeIdx == GUI_ITEM_TYPE.VEHICLE:
            return self.__getVehiclesData(dataIdx)
        if itemTypeIdx == GUI_ITEM_TYPE.TANKMAN:
            return self.__getTankmenData(dataIdx)
        if itemTypeIdx == GUI_ITEM_TYPE.CUSTOMIZATION:
            return self.__getCustomizationsData(dataIdx)
        return self.__getItemsData(itemTypeIdx, dataIdx)

    def getFreeSlots(self, vehiclesSlots):
        return vehiclesSlots - len(self.__getVehiclesData())

    @async
    def _requestCache(self, callback = None):
        BigWorld.player().inventory.getCache(lambda resID, value: self._response(resID, value, callback))

    def _response(self, resID, invData, callback = None):
        self.__vehsCDsByID = {}
        if invData is not None:
            for invID, vCompDescr in invData[GUI_ITEM_TYPE.VEHICLE]['compDescr'].iteritems():
                self.__vehsCDsByID[invID] = vehicles.makeIntCompactDescrByID('vehicle', *vehicles.parseVehicleCompactDescr(vCompDescr))

        self.__vehsIDsByCD = dict(((v, k) for k, v in self.__vehsCDsByID.iteritems()))
        super(InventoryRequester, self)._response(resID, invData, callback)
        return

    def __getItemsData(self, itemTypeIdx, compactDescr = None):
        """
        Common items request handler. Returns all given type items
        data or only one specific data by @compactDescr.
        
        @param itemTypeIdx: item type index from common.items.ITEM_TYPE_NAMES
        @param compactDescr: item int compact descriptor
        @return dictionary of all items data or one item data
        """
        result = self.getCacheValue(itemTypeIdx)
        if result is not None and compactDescr is not None:
            return result.get(compactDescr)
        else:
            return result

    def __makeItem(self, itemTypeID, invDataIdx):
        return self.__getMaker(itemTypeID)(invDataIdx)

    def __getMaker(self, itemTypeID):
        if itemTypeID == GUI_ITEM_TYPE.VEHICLE:
            return self.__makeVehicle
        if itemTypeID == GUI_ITEM_TYPE.TANKMAN:
            return self.__makeTankman
        return self.__makeSimpleItem

    def __makeVehicle(self, vehInvID):
        if vehInvID not in self.__vehsCDsByID:
            return
        else:
            typeCompDescr = self.__vehsCDsByID[vehInvID]
            cache = self.__itemsCache[GUI_ITEM_TYPE.VEHICLE]
            if typeCompDescr in cache:
                return cache[typeCompDescr]
            itemsInvData = self.getCacheValue(GUI_ITEM_TYPE.VEHICLE, {})

            def value(key, default = None):
                return itemsInvData.get(key, {}).get(vehInvID, default)

            compactDescr = value('compDescr')
            if compactDescr is None:
                return
            try:
                item = cache[typeCompDescr] = self.VEH_DATA(value('compDescr'), vehicles.VehicleDescr(compactDescr=compactDescr), vehInvID, value('repair', 0), value('crew', []), value('lock', 0), value('settings', 0), value('shells', []), value('shellsLayout', []), value('eqs', []), value('eqsLayout', []))
            except Exception:
                LOG_DEBUG('Error while building vehicle from inventory', vehInvID, typeCompDescr)
                return

            return item

    def __makeTankman(self, tmanInvID):
        cache = self.__itemsCache[GUI_ITEM_TYPE.TANKMAN]
        if tmanInvID in cache:
            return cache[tmanInvID]
        else:
            itemsInvData = self.getCacheValue(GUI_ITEM_TYPE.TANKMAN, {})

            def value(key, default = None):
                return itemsInvData.get(key, {}).get(tmanInvID, default)

            compactDescr = value('compDescr')
            if compactDescr is None:
                return
            item = cache[tmanInvID] = self.TMAN_DATA(compactDescr, tankmen.TankmanDescr(compactDescr), value('vehicle', -1), tmanInvID)
            return item

    def __makeSimpleItem(self, typeCompDescr):
        itemTypeID = getTypeOfCompactDescr(typeCompDescr)
        cache = self.__itemsCache[itemTypeID]
        if typeCompDescr in cache:
            return cache[typeCompDescr]
        else:
            itemsInvData = self.getCacheValue(itemTypeID, {})
            if typeCompDescr not in itemsInvData:
                return None
            data = self.ITEM_DATA(typeCompDescr, vehicles.getItemByCompactDescr(typeCompDescr), itemsInvData[typeCompDescr])
            item = cache[typeCompDescr] = data
            return item

    def __makeOutfit(self, intCD, season):
        cache = self.__itemsCache[GUI_ITEM_TYPE.OUTFIT]
        if (intCD, season) in cache:
            return cache[intCD, season]
        else:
            invData = self.getCacheValue(GUI_ITEM_TYPE.CUSTOMIZATION, {})
            outfitsData = invData.get(CustomizationInvData.OUTFITS, {})
            vehicleOutfits = outfitsData.get(intCD, {})
            if season not in vehicleOutfits:
                return None
            compDescr, isEnabled = vehicleOutfits.get(season)
            item = cache[intCD, season] = self.OUTFIT_DATA(compDescr, isEnabled)
            return item

    def __getTankmenData(self, inventoryID = None):
        """
        Tankmen inventory data request handler. Returns all tankmen
        data or specific tankman data by given inventory id.
        
        @param inventoryID: optional tankman inventory id
        @return: all tankmen data or only specific tankmen data as dict
        """
        tankmanItemsData = self.__getItemsData(vehicles._TANKMAN)
        if tankmanItemsData is None:
            return
        elif inventoryID is not None:
            return self.__getTankmanData(tankmanItemsData, inventoryID)
        else:
            result = dict()
            for invID in tankmanItemsData.get('compDescr', dict()).iterkeys():
                result[invID] = self.__getTankmanData(tankmanItemsData, invID)

            return result

    def __getTankmanData(self, tankmanItemsData, invID):
        """
        Helper-method to collect tankman data-dict from given raw
        inventory data
        
        @param tankmanItemsData: raw tankman inventory data
        @param invID: tankman inventory id
        @return: tankman data-dict
        """
        if invID not in tankmanItemsData['compDescr'].keys():
            return
        else:
            result = dict()
            for key, values in tankmanItemsData.iteritems():
                value = values.get(invID)
                if value is not None:
                    result[key] = value

            return result

    def __getVehiclesData(self, inventoryID = None):
        """
        Vehicles inventory data request handler. Returns all vehicles
        data or specific vehicle data by given inventory id.
        
        @param inventoryID: optional vehicle inventory id
        @return: all vehicles data or only specific vehicle data as dict
        """
        vehItemsData = self.__getItemsData(vehicles._VEHICLE)
        if vehItemsData is None:
            return
        elif inventoryID is not None:
            return self.__getVehicleData(vehItemsData, inventoryID)
        else:
            result = dict()
            for invID in vehItemsData.get('compDescr', dict()).iterkeys():
                result[invID] = self.__getVehicleData(vehItemsData, invID)

            return result

    def __getVehicleData(self, vehItemsData, invID):
        """
        Helper-method to collect vehicle data-dict from given raw
        inventory data
        
        @param vehItemsData: raw vehicle inventory data
        @param invID: vehicle inventory id
        @return: vehicle data-dict
        """
        if invID not in vehItemsData['compDescr'].keys():
            return
        else:
            result = dict()
            for key, values in vehItemsData.iteritems():
                value = values.get(invID)
                if value is not None:
                    result[key] = value

            return result

    def __getCustomizationsData(self, intCD):
        _, cType, idx = parseIntCompactDescr(intCD)
        customizationInvData = self.getCacheValue(GUI_ITEM_TYPE.CUSTOMIZATION, {})
        itemsInvData = customizationInvData.get(CustomizationInvData.ITEMS, {})
        typeInvData = itemsInvData.get(cType, {})
        return typeInvData.get(idx, {})