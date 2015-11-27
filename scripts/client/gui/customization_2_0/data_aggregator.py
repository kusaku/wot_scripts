# Embedded file name: scripts/client/gui/customization_2_0/data_aggregator.py
from Event import Event
from constants import IGR_TYPE
from debug_utils import LOG_DEBUG
from gui.game_control import getIGRCtrl
from gui.shared import g_itemsCache as _g_itemsCache
from gui.shared.ItemsCache import CACHE_SYNC_REASON
from items.vehicles import g_cache as _g_vehiclesCache
from items.qualifiers import g_cache as _g_qualifiersCache
from CurrentVehicle import g_currentVehicle as _g_currentVehicle
from elements import AvailableCamouflage, AvailableInscription, AvailableEmblem, InstalledCamouflage, InstalledInscription, InstalledEmblem, Qualifier, CamouflageQualifier

class CUSTOMIZATION_TYPE:
    CAMOUFLAGE = 0
    EMBLEM = 1
    INSCRIPTION = 2


SLOT_TYPE = {CUSTOMIZATION_TYPE.EMBLEM: 'player',
 CUSTOMIZATION_TYPE.INSCRIPTION: 'inscription'}
_MAX_HULL_SLOTS = 2
_MAX_TURRET_SLOTS = 2

class DataAggregator(object):

    def __init__(self):
        self.updated = Event()
        self.viewModel = None
        self.__installed = None
        self.__available = None
        self.__purchased = None
        self.__initialViewModel = None
        self.__updateCurrentVehicleCustomization(CACHE_SYNC_REASON.DOSSIER_RESYNC, None)
        _g_itemsCache.onSyncCompleted += self.__updateCurrentVehicleCustomization
        return

    def fini(self):
        _g_currentVehicle.onChanged -= self.__updateCurrentVehicleCustomization
        self.__installed = None
        self.__available = None
        self.__purchased = None
        self.__initialViewModel = None
        self.viewModel = None
        return

    @property
    def installed(self):
        return self.__installed

    @property
    def available(self):
        return self.__available

    @property
    def initialViewModel(self):
        return self.__initialViewModel

    def __updateCurrentVehicleCustomization(self, updateReason, invalidItems):
        if updateReason in (CACHE_SYNC_REASON.DOSSIER_RESYNC, CACHE_SYNC_REASON.SHOP_RESYNC):
            curVehItem = _g_currentVehicle.item
            curVehDescr = curVehItem.descriptor
            self.__initialViewModel = (curVehDescr.playerEmblems, curVehDescr.playerInscriptions)
            self.viewModel = [list(curVehDescr.camouflages), list(curVehDescr.playerEmblems), list(curVehDescr.playerInscriptions)]
            self.__available = self.__setAvailableCustomization(curVehItem)
            self.__installed = self.__setInstalledCustomization(curVehDescr)
            self.updated()

    def __setInstalledCustomization(self, curVehDescr):
        vehicleHullSlots = curVehDescr.hull['emblemSlots']
        vehicleTurretSlots = curVehDescr.turret['emblemSlots']
        installedHullEmblems = []
        installedTurretEmblems = []
        installedHullInscriptions = []
        installedTurretInscriptions = []
        hullEmblemSlotIdx = 0
        hullInscriptionSlotIdx = 0
        turretEmblemSlotIdx = 0
        turretInscriptionSlotIdx = 0
        for slot in vehicleHullSlots:
            if slot.type == SLOT_TYPE[CUSTOMIZATION_TYPE.EMBLEM]:
                installedHullEmblems.append(curVehDescr.playerEmblems[hullEmblemSlotIdx])
                hullEmblemSlotIdx += 1
            if slot.type == SLOT_TYPE[CUSTOMIZATION_TYPE.INSCRIPTION]:
                installedHullInscriptions.append(curVehDescr.playerInscriptions[hullInscriptionSlotIdx])
                hullInscriptionSlotIdx += 1

        for slot in vehicleTurretSlots:
            if slot.type == SLOT_TYPE[CUSTOMIZATION_TYPE.EMBLEM]:
                installedTurretEmblems.append(curVehDescr.playerEmblems[_MAX_HULL_SLOTS + turretEmblemSlotIdx])
                turretEmblemSlotIdx += 1
            if slot.type == SLOT_TYPE[CUSTOMIZATION_TYPE.INSCRIPTION]:
                installedTurretInscriptions.append(curVehDescr.playerInscriptions[_MAX_HULL_SLOTS + turretInscriptionSlotIdx])
                turretInscriptionSlotIdx += 1

        return ([ InstalledCamouflage(ic, 0, self.__available[CUSTOMIZATION_TYPE.CAMOUFLAGE][ic[0]].qualifier if ic[0] is not None else None) for ic in curVehDescr.camouflages ], [ InstalledEmblem(ihe, 0, self.__available[CUSTOMIZATION_TYPE.EMBLEM][ihe[0]].qualifier if ihe[0] is not None else None) for ihe in installedHullEmblems ] + [ InstalledEmblem(ite, 2, self.__available[CUSTOMIZATION_TYPE.EMBLEM][ite[0]].qualifier if ite[0] is not None else None) for ite in installedTurretEmblems ], [ InstalledInscription(ihi, 0, self.__available[CUSTOMIZATION_TYPE.INSCRIPTION][ihi[0]].qualifier if ihi[0] is not None else None) for ihi in installedHullInscriptions ] + [ InstalledInscription(iti, 2, self.__available[CUSTOMIZATION_TYPE.INSCRIPTION][iti[0]].qualifier if iti[0] is not None else None) for iti in installedTurretInscriptions ])

    def __setAvailableCustomization(self, curVehItem):
        availableEmblems = {}
        availableInscriptions = {}
        availableCamouflages = {}
        igrType = getIGRCtrl().getRoomType() if getIGRCtrl().getRoomType() != IGR_TYPE.NONE else -1
        purchased = (_g_itemsCache.items.getVehicleDossier(curVehItem.intCD).getBlock('camouflages'), _g_itemsCache.items.getVehicleDossier(curVehItem.intCD).getBlock('emblems'), _g_itemsCache.items.getVehicleDossier(curVehItem.intCD).getBlock('inscriptions'))
        LOG_DEBUG('\n\n =========================== \n\n')
        LOG_DEBUG(_g_vehiclesCache.playerEmblems()[0])
        LOG_DEBUG(_g_vehiclesCache.playerEmblems()[1])
        LOG_DEBUG(_g_vehiclesCache.customization(curVehItem.nationID)['inscriptionGroups'])
        LOG_DEBUG(_g_vehiclesCache.customization(curVehItem.nationID)['inscriptions'])
        LOG_DEBUG(_g_vehiclesCache.customization(curVehItem.nationID)['camouflages'])
        LOG_DEBUG('\n\n =========================== \n\n')
        inscriptionGroups = _g_vehiclesCache.customization(curVehItem.nationID)['inscriptionGroups']
        emblemGroups = _g_vehiclesCache.playerEmblems()[0]
        for emblemID, availableEmblem in _g_vehiclesCache.playerEmblems()[1].iteritems():
            if availableEmblem[7] in _g_qualifiersCache.qualifiers:
                qualifier = Qualifier(_g_qualifiersCache.qualifiers[availableEmblem[7]])
            else:
                qualifier = CamouflageQualifier()
            allowedVehicles = emblemGroups[availableEmblem[0]][3]
            notAllowedVehicles = emblemGroups[availableEmblem[0]][4]
            availableEmblems[emblemID] = AvailableEmblem(emblemID, availableEmblem, qualifier, emblemID in purchased[CUSTOMIZATION_TYPE.EMBLEM] or availableEmblem[1] == igrType, allowedVehicles, notAllowedVehicles)

        for inscriptionID, availableInscription in _g_vehiclesCache.customization(curVehItem.nationID)['inscriptions'].iteritems():
            if availableEmblem[7] in _g_qualifiersCache.qualifiers:
                qualifier = Qualifier(_g_qualifiersCache.qualifiers[availableEmblem[7]])
            else:
                qualifier = CamouflageQualifier()
            allowedVehicles = inscriptionGroups[availableInscription[0]][3]
            notAllowedVehicles = inscriptionGroups[availableInscription[0]][4]
            availableInscriptions[inscriptionID] = AvailableInscription(inscriptionID, availableInscription, qualifier, inscriptionID in purchased[CUSTOMIZATION_TYPE.INSCRIPTION] or availableInscription[1] == igrType, allowedVehicles, notAllowedVehicles)

        for camouflageID, availableCamouflage in _g_vehiclesCache.customization(curVehItem.nationID)['camouflages'].iteritems():
            availableCamouflages[camouflageID] = AvailableCamouflage(camouflageID, availableCamouflage, CamouflageQualifier(), camouflageID in purchased[CUSTOMIZATION_TYPE.CAMOUFLAGE] or availableCamouflage['igrType'] == igrType, availableCamouflage['allow'], availableCamouflage['deny'])

        return (availableCamouflages, availableEmblems, availableInscriptions)