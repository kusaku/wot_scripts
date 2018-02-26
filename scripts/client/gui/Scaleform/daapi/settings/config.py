# Embedded file name: scripts/client/gui/Scaleform/daapi/settings/config.py
from constants import HAS_DEV_RESOURCES, ARENA_GUI_TYPE
_COMMON_RELEASE_PACKAGES = ('gui.Scaleform.daapi.view.common',)
_COMMON_DEBUG_PACKAGES = ('gui.development.ui.GUIEditor',)
_LOBBY_RELEASE_PACKAGES = ('gui.Scaleform.daapi.view.lobby', 'gui.Scaleform.daapi.view.lobby.barracks', 'gui.Scaleform.daapi.view.lobby.boosters', 'gui.Scaleform.daapi.view.lobby.clans', 'gui.Scaleform.daapi.view.lobby.crewOperations', 'gui.Scaleform.daapi.view.lobby.customization', 'gui.Scaleform.daapi.view.lobby.cyberSport', 'gui.Scaleform.daapi.view.lobby.exchange', 'gui.Scaleform.daapi.view.lobby.fortifications', 'gui.Scaleform.daapi.view.lobby.hangar', 'gui.Scaleform.daapi.view.lobby.header', 'gui.Scaleform.daapi.view.lobby.inputChecker', 'gui.Scaleform.daapi.view.lobby.messengerBar', 'gui.Scaleform.daapi.view.lobby.prb_windows', 'gui.Scaleform.daapi.view.lobby.profile', 'gui.Scaleform.daapi.view.lobby.rankedBattles', 'gui.Scaleform.daapi.view.lobby.store', 'gui.Scaleform.daapi.view.lobby.techtree', 'gui.Scaleform.daapi.view.lobby.trainings', 'gui.Scaleform.daapi.view.lobby.vehiclePreview', 'gui.Scaleform.daapi.view.lobby.vehicle_compare', 'gui.Scaleform.daapi.view.lobby.wgnc', 'gui.Scaleform.daapi.view.login', 'messenger.gui.Scaleform.view.lobby', 'gui.Scaleform.daapi.view.lobby.missions.regular', 'gui.Scaleform.daapi.view.lobby.missions.personal', 'gui.Scaleform.daapi.view.bootcamp.lobby', 'gui.Scaleform.daapi.view.lobby.event_boards', 'gui.Scaleform.daapi.view.lobby.ny')
_LOBBY_DEBUG_PACKAGES = ('gui.development.ui.messenger.view.lobby',)
_BATTLE_RELEASE_PACKAGES = ('gui.Scaleform.daapi.view.battle.shared', 'messenger.gui.Scaleform.view.battle')
_BATTLE_DEBUG_PACKAGES = ('gui.development.ui.battle',)
LOBBY_PACKAGES = _LOBBY_RELEASE_PACKAGES
BATTLE_PACKAGES = _BATTLE_RELEASE_PACKAGES
COMMON_PACKAGES = _COMMON_RELEASE_PACKAGES
BATTLE_PACKAGES_BY_ARENA_TYPE = {ARENA_GUI_TYPE.FALLOUT_CLASSIC: ('gui.Scaleform.daapi.view.battle.fallout',),
 ARENA_GUI_TYPE.FALLOUT_MULTITEAM: ('gui.Scaleform.daapi.view.battle.fallout',),
 ARENA_GUI_TYPE.TUTORIAL: ('gui.Scaleform.daapi.view.battle.tutorial',),
 ARENA_GUI_TYPE.EVENT_BATTLES: ('gui.Scaleform.daapi.view.battle.event',),
 ARENA_GUI_TYPE.RANKED: ('gui.Scaleform.daapi.view.battle.ranked',),
 ARENA_GUI_TYPE.BOOTCAMP: ('gui.Scaleform.daapi.view.bootcamp.battle',),
 ARENA_GUI_TYPE.EPIC_RANDOM: ('gui.Scaleform.daapi.view.battle.epic_random',),
 ARENA_GUI_TYPE.EPIC_RANDOM_TRAINING: ('gui.Scaleform.daapi.view.battle.epic_random',)}
BATTLE_PACKAGES_BY_DEFAULT = ('gui.Scaleform.daapi.view.battle.classic',)
if HAS_DEV_RESOURCES:
    LOBBY_PACKAGES += _LOBBY_DEBUG_PACKAGES
    BATTLE_PACKAGES += _BATTLE_DEBUG_PACKAGES
    COMMON_PACKAGES += _COMMON_DEBUG_PACKAGES