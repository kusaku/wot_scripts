# Embedded file name: scripts/client/gui/shared/gui_items/dossier/achievements/validators.py
from helpers import dependency
from skeletons.gui.server_events import IEventsCache

def questHasThisAchievementAsBonus(name, block):
    eventsCache = dependency.instance(IEventsCache)
    for records in eventsCache.getQuestsDossierBonuses().itervalues():
        if (block, name) in records:
            return True

    return False


def alreadyAchieved(achievementClass, name, block, dossier):
    return achievementClass.checkIsInDossier(block, name, dossier)


def requiresFortification():
    from gui.LobbyContext import g_lobbyContext
    return g_lobbyContext.getServerSettings() is not None and g_lobbyContext.getServerSettings().isStrongholdsEnabled()


def accountIsRoaming(dossier):
    return dossier.isInRoaming()