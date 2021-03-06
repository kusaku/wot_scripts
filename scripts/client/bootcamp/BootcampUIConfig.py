# Embedded file name: scripts/client/bootcamp/BootcampUIConfig.py
from collections import namedtuple
import ResMgr
from copy import copy
import resource_helper
from debug_utils_bootcamp import LOG_DEBUG_DEV_BOOTCAMP
g_defaultBattleUiSettings = {'hideDebugPanel': True,
 'hideTeamBasesPanel': True,
 'hideSixthSence': True,
 'hideConsumablesPanel': True,
 'hideDestroyTimersPanel': True,
 'hideBattleTickerPanel': True,
 'hideBattleMessagenger': True,
 'hideFragCorrelationBar': True,
 'hideFullStats': True,
 'hidePlayersPanel': True,
 'hideRadialMenu': True,
 'hideEndWarningPanel': True,
 'hideMinimap': True,
 'hidePreBattleTimer': True,
 'hideRibbonsPanel': True,
 'hideBattleTimer': True,
 'hideDamageInfoPanel': True,
 'hideDamageLogPanel': True}
g_defaultLobbyUiSettings = {'hideMessagenger': True,
 'hideHeader': True,
 'hideHeaderSettings': False,
 'hideHeaderAccount': False,
 'hideHeaderPremium': True,
 'hideHeaderSquad': True,
 'hideHeaderBattleSelector': True,
 'hideHeaderGold': True,
 'hideHeaderSilver': True,
 'hideHeaderFreeExp': True,
 'hideHeaderFightButton': False,
 'hideHeaderMainMenuButtonBar': True,
 'hideMenuHangar': True,
 'hideMenuShop': True,
 'hideMenuProfile': True,
 'hideMenuTechTree': True,
 'hideMenuBarracks': True,
 'hideMenuBrowser': True,
 'hideMenuForts': True,
 'hideMenuMissions': True,
 'hideMenuAcademy': True,
 'hideHangarVehResearchPanel': True,
 'hideHangarTmenXpPanel': True,
 'hideHangarCrewOperations': True,
 'hideHangarCrew': True,
 'hideHangarParams': True,
 'hideHangarAmmunitionPanel': False,
 'hideHangarCarousel': True,
 'hideHangarIgr': True,
 'hideHangarQuestControl': True,
 'hideHangarServerInfo': True,
 'hideHangarSwitchModePanel': True,
 'hideHangarHeader': True,
 'hideHangarVehicleState': True,
 'hideHangarMaintenanceButtons': True,
 'hideHangarComponents': True,
 'hideHangarOptionalDevices': True,
 'hideHangarShells': True,
 'hideHangarEquipment': True,
 'showHangarTooltip0': True}
g_defaultBattleRibbonsSettings = {'damage': False,
 'kill': False,
 'armor': False,
 'ram': False,
 'spotted': False,
 'capture': False,
 'crits': False}
XML_CONFIG_PATH = 'scripts/bootcamp_docs/battle_page_visibility.xml'

def readUISettingsFile(path):
    settingsConfig = ResMgr.openSection(path)
    if settingsConfig is None:
        raise Exception("Can't open config file (%s)" % path)
    allPrebattleSettings = {}
    allBattleSettings = {}
    allGarageSettings = {}
    allRibbonsSettings = {}
    for name, section in settingsConfig.items():
        if name == 'lesson':
            lessonId = section['id'].asInt
            lobbySettings = copy(g_defaultLobbyUiSettings)
            visString = section['visible_garage'].asString
            visibilityNames = visString.split()
            for visName in visibilityNames:
                hideName = 'hide' + visName
                if hideName in lobbySettings:
                    lobbySettings[hideName] = False
                else:
                    showName = 'show' + visName
                    if showName in lobbySettings:
                        lobbySettings[showName] = True
                    else:
                        LOG_DEBUG_DEV_BOOTCAMP('Unknown setting name (%s)' % hideName)

            allGarageSettings[lessonId] = lobbySettings
            battleSettings = copy(g_defaultBattleUiSettings)
            visString = section['visible_battle'].asString
            visibilityNames = visString.split()
            for visName in visibilityNames:
                hideName = 'hide' + visName
                if hideName in battleSettings:
                    battleSettings[hideName] = False
                else:
                    showName = 'show' + visName
                    if showName in battleSettings:
                        battleSettings[showName] = True
                    else:
                        LOG_DEBUG_DEV_BOOTCAMP('Unknown setting name (%s)' % hideName)

            allBattleSettings[lessonId] = battleSettings
            ribbonsSettings = copy(g_defaultBattleRibbonsSettings)
            ribString = section['ribbons'].asString
            ribbonNames = ribString.split()
            for ribName in ribbonNames:
                if ribName in ribbonsSettings:
                    ribbonsSettings[ribName] = True

            allRibbonsSettings[lessonId] = ribbonsSettings
            prebattleSettings = {}
            prebattleSection = section['prebattle']
            if prebattleSection.has_key('timeout'):
                prebattleSettings['timeout'] = prebattleSection['timeout'].asFloat
            allPrebattleSettings[lessonId] = prebattleSettings

    return (allPrebattleSettings,
     allRibbonsSettings,
     allBattleSettings,
     allGarageSettings)


g_prebattleSettings, g_battleRibbonsSettings, g_battleUiSettings, g_lobbyUiSettings = readUISettingsFile(XML_CONFIG_PATH)

class _BootcampManagerObserverConfig(namedtuple('_BootcampManagerObserverConfig', ['viewClassName', 'observerClassName', 'daapiAlias'])):

    def getVO(self):
        return self._asdict()


def readBootcampManagerConfig(xmlPath):
    observers = []
    ctx, section = resource_helper.getRoot(xmlPath)
    for ctx, subSection in resource_helper.getIterator(ctx, section['observers']):
        item = resource_helper.readItem(ctx, subSection)
        if not item.name:
            continue
        if 'observerClassName' not in item.value or not item.value['observerClassName']:
            raise Exception('Empty observer class name', item)
        if 'daapiAlias' not in item.value or not item.value['daapiAlias']:
            raise Exception('Empty daapiAlias', item)
        observer = _BootcampManagerObserverConfig(item.name, item.value['observerClassName'], item.value['daapiAlias'])
        observers.append(observer)

    return {'observers': observers}


def getBattleUISettings(lessonId):
    return g_battleUiSettings[lessonId]


def getBattleRibbonsSettings(lessonId):
    return g_battleRibbonsSettings[lessonId]


def getPrebattleSettings(lessonId):
    return g_prebattleSettings[lessonId]


def getLobbyUISettings(lessonId):
    LOG_DEBUG_DEV_BOOTCAMP('getLobbyUISettings, lesson - ', lessonId)
    return g_lobbyUiSettings[lessonId]