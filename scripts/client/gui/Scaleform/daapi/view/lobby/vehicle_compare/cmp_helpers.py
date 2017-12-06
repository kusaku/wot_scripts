# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/vehicle_compare/cmp_helpers.py
import operator
import time
from gui.Scaleform.daapi.view.lobby.vehicle_compare.cmp_top_modules import TopModulesChecker
from gui.game_control.veh_comparison_basket import PARAMS_AFFECTED_TANKMEN_SKILLS
from helpers import dependency
from items import tankmen
from items.components.c11n_components import SeasonType
from debug_utils import LOG_WARNING
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.framework import ViewTypes
from gui.Scaleform.framework.managers.containers import POP_UP_CRITERIA
from gui.app_loader.loader import g_appLoader
from gui.shared.gui_items import GUI_ITEM_TYPE_NAMES, GUI_ITEM_TYPE
from gui.shared.gui_items.Tankman import Tankman
from shared_utils import first
from skeletons.gui.customization import ICustomizationService
from skeletons.gui.shared import IItemsCache
from skeletons.gui.shared.gui_items import IGuiItemsFactory
MODULES_INSTALLING_ORDER = (GUI_ITEM_TYPE.CHASSIS,
 GUI_ITEM_TYPE.TURRET,
 GUI_ITEM_TYPE.GUN,
 GUI_ITEM_TYPE.ENGINE,
 GUI_ITEM_TYPE.RADIO)
NOT_AFFECTED_DEVICES = {}
NOT_AFFECTED_EQUIPMENTS = {'handExtinguishers',
 'autoExtinguishers',
 'smallMedkit',
 'largeMedkit',
 'smallRepairkit',
 'largeRepairkit'}
OPTIONAL_DEVICE_TYPE_NAME = GUI_ITEM_TYPE_NAMES[GUI_ITEM_TYPE.OPTIONALDEVICE]
EQUIPMENT_TYPE_NAME = GUI_ITEM_TYPE_NAMES[GUI_ITEM_TYPE.EQUIPMENT]
BATTLE_BOOSTER_TYPE_NAME = GUI_ITEM_TYPE_NAMES[GUI_ITEM_TYPE.BATTLE_BOOSTER]

def createTankman(nationID, vehicleTypeID, role, roleLevel, skills):
    """
    Generates tankmen with provided parameters
    :param nationID: *.nations.INDICES
    :param vehicleTypeID: int
    :param role: *.Tankman.ROLES
    :param roleLevel: *.CREW_TYPES
    :param skills: the set of skills
    :return: gui.shared.gui_items.Tankman
    """
    descr = tankmen.generateCompactDescr(tankmen.generatePassport(nationID), vehicleTypeID, role, roleLevel, skills)
    return Tankman(descr)


def sortSkills(skillsSet):
    """
    Sorts provided set of skills in order from PARAMS_AFFECTED_TANKMEN_SKILLS
    :param skillsSet: set of skills
    :return: sorted set of skills
    """
    return sorted(skillsSet, key=lambda skill: PARAMS_AFFECTED_TANKMEN_SKILLS.index(skill))


def _getAvailableSkillsByRoles(availableSkills):
    """
    Links tankmens roles with available skills for this roles
    :param availableSkills:
    :return:
    """
    outcome = {}
    for role, skills in tankmen.SKILLS_BY_ROLES.iteritems():
        intersection = skills.intersection(set(availableSkills))
        if intersection:
            outcome[role] = intersection

    return outcome


_PARAMS_AFFECTED_SKILLS_BY_ROLES = _getAvailableSkillsByRoles(PARAMS_AFFECTED_TANKMEN_SKILLS)

def getVehicleCrewSkills(vehicle):
    """
    Generates the list of skills for tankmen roles from provided vehicle (items in list in the vehicle roles order)
    :param vehicle: target Vehicle
    :return: the list of roles and skills related to this roles:
    [['commander', frozenset(['commander_eagleEye', 'camouflage', ...])], ...]
    """
    descCrewRoles = vehicle.descriptor.type.crewRoles
    mainRoles = map(operator.itemgetter(0), descCrewRoles)
    outcome = map(lambda role: [role, _PARAMS_AFFECTED_SKILLS_BY_ROLES[role]], mainRoles)
    leftRoles = set(tankmen.ROLES.difference(set(mainRoles)))
    if leftRoles:
        for idx, rolesRange in reversed(list(enumerate(descCrewRoles))):
            for role in rolesRange:
                if role in leftRoles:
                    leftRoles.remove(role)
                    outcome[idx][1] |= _PARAMS_AFFECTED_SKILLS_BY_ROLES[role]
                    if not leftRoles:
                        return outcome

    else:
        return outcome


@dependency.replace_none_kwargs(itemsCache=IItemsCache)
def getVehCrewInfo(vehIntCD, itemsCache = None):
    levelsByIndexes = {}
    nativeVehiclesByIndexes = {}
    hangarVehicle = itemsCache is not None and itemsCache.items.getItemByCD(vehIntCD)
    if not hangarVehicle.itemTypeID == GUI_ITEM_TYPE.VEHICLE:
        raise AssertionError
        for roleIdx, tankmen in hangarVehicle.crew:
            if tankmen:
                levelsByIndexes[roleIdx] = int(tankmen.roleLevel)
                nativeVehiclesByIndexes[roleIdx] = itemsCache.items.getItemByCD(tankmen.vehicleNativeDescr.type.compactDescr)

    return (levelsByIndexes, nativeVehiclesByIndexes)


def createTankmans(crewData):
    return map(lambda strCD: (strCD[0], Tankman(strCD[1]) if strCD[1] else None), crewData)


@dependency.replace_none_kwargs(itemsCache=IItemsCache)
def installEquipmentOnVehicle(vehicle, intCD, slotIndex, itemsCache = None):
    """
    Installs equipement on the provided vehicle in particular slot
    :param vehicle: target Vehicle
    :param intCD: equipment intCD
    :param slotIndex: 0, 1, 2 - indexes
    :return:
    """
    if intCD and itemsCache is not None:
        equipment = itemsCache.items.getItemByCD(int(intCD))
    else:
        equipment = None
    if not (equipment and equipment.itemTypeID == GUI_ITEM_TYPE.EQUIPMENT):
        raise AssertionError('Invalid type of item: {}'.format(equipment.itemTypeID))
        success, reason = equipment.mayInstall(vehicle, slotIndex)
        if not success:
            LOG_WARNING('Equipment could not installed, reason: '.format(reason))
            return
    vehicle.equipment.regularConsumables[slotIndex] = equipment
    vehicle.equipmentLayout.regularConsumables[slotIndex] = equipment
    return


@dependency.replace_none_kwargs(itemsCache=IItemsCache)
def installBattleBoosterOnVehicle(vehicle, intCD, itemsCache = None):
    if intCD and itemsCache is not None:
        booster = itemsCache.items.getItemByCD(int(intCD))
    else:
        booster = None
    vehicle.equipment.battleBoosterConsumables[0] = booster
    return


def isEquipmentSame(equipment1, equipment2):
    if equipment1 is None or equipment2 is None:
        return False
    elif len(equipment1) != len(equipment2):
        return False
    else:
        for i in xrange(len(equipment1)):
            if equipment1[i] != equipment2[i]:
                return False

        return True


def getCmpConfiguratorMainView():
    """
    Provides reference on vehicle configurator view.
    :return:
    """
    cmpConfiguratorMain = g_appLoader.getApp().containerManager.getView(ViewTypes.LOBBY_SUB, {POP_UP_CRITERIA.VIEW_ALIAS: VIEW_ALIAS.VEHICLE_COMPARE_MAIN_CONFIGURATOR})
    raise cmpConfiguratorMain is not None or AssertionError
    return cmpConfiguratorMain


@dependency.replace_none_kwargs(c11nService=ICustomizationService)
def getSuitableCamouflage(vehicle, c11nService = None):
    return first(c11nService.getCamouflages(vehicle=vehicle).itervalues())


def isCamouflageSet(vehicle):
    return bool(vehicle.getBonusCamo())


@dependency.replace_none_kwargs(factory=IGuiItemsFactory)
def applyCamouflage(vehicle, select, factory = None):
    if select:
        camo = getSuitableCamouflage(vehicle)
        if camo:
            outfit = vehicle.getCustomOutfit(camo.season)
            outfit = outfit or factory.createOutfit(isEnabled=True)
            outfit.hull.slotFor(GUI_ITEM_TYPE.CAMOUFLAGE).set(camo)
            vehicle.setCustomOutfit(camo.season, outfit)
    else:
        removeVehicleCamouflages(vehicle)


def removeVehicleCamouflages(vehicle):
    for season in SeasonType.SEASONS:
        outfit = vehicle.getOutfit(season)
        if outfit:
            outfit.hull.slotFor(GUI_ITEM_TYPE.CAMOUFLAGE).clear()


def getVehicleModules(vehicle):
    return (vehicle.chassis,
     vehicle.turret,
     vehicle.gun,
     vehicle.engine,
     vehicle.radio)


def getVehicleTopModules(vehicle):
    checker = TopModulesChecker(vehicle)
    topMoudles = checker.process()
    checker.clear()
    return sorted(topMoudles, key=lambda module: MODULES_INSTALLING_ORDER.index(module.itemTypeID))