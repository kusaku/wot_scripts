# Embedded file name: scripts/client/gui/server_events/settings.py
import time
from gui.shared import utils, events, g_eventBus
_LAST_PQ_INTRO_VERSION = 'fallout'

class _PMSettings(utils.SettingRecord):

    def __init__(self, introShown = False, operationsVisited = set(), headerAlert = False):
        super(_PMSettings, self).__init__(introShown=introShown, operationsVisited=operationsVisited, headerAlert=headerAlert)

    def markOperationAsVisited(self, operationID):
        self.update(operationsVisited=self.operationsVisited | {operationID})


class _QuestSettings(utils.SettingRootRecord):

    def __init__(self, lastVisitTime = -1, visited = set(), naVisited = set(), minimized = set(), personalMissions = None):
        super(_QuestSettings, self).__init__(lastVisitTime=lastVisitTime, visited=visited, naVisited=naVisited, minimized=minimized, personalMissions=_PMSettings(**(personalMissions or {})))

    def updateVisited(self, visitSettingName, eventID):
        settingsValue = set(self[visitSettingName])
        if eventID not in settingsValue:
            self.update(**{visitSettingName: tuple(settingsValue | {eventID})})
            return True
        return False

    def removeCompleted(self, completedIDs):
        self.update(visited=tuple(set(self.visited).difference(completedIDs)))
        self.update(naVisited=tuple(set(self.naVisited).difference(completedIDs)))

    def updateExpanded(self, eventID, isExpanded):
        settingsValue = set(self['minimized'])
        if isExpanded:
            self.update(minimized=tuple(settingsValue.difference([eventID])))
        else:
            self.update(minimized=tuple(settingsValue.union([eventID])))

    def save(self):
        self.update(lastVisitTime=time.time())
        super(_QuestSettings, self).save()

    def _asdict(self):
        result = super(_QuestSettings, self)._asdict()
        result.update(personalMissions=self.personalMissions._asdict())
        return result

    @classmethod
    def _getSettingName(cls):
        return 'quests'


def get():
    return _QuestSettings.load()


def isNewCommonEvent(svrEvent, settings = None):
    settings = settings or get()
    if svrEvent.isAvailable()[0]:
        setting = 'visited'
    else:
        setting = 'naVisited'
    return svrEvent.getID() not in settings[setting] and not svrEvent.isCompleted() and not svrEvent.isOutOfDate()


def isGroupMinimized(groupID, settings = None):
    settings = settings or get()
    return groupID in settings['minimized']


def getNewCommonEvents(events):
    """ Acquire subset of not viewed events from the given events.
    """
    settings = get()
    return filter(lambda e: isNewCommonEvent(e, settings), events)


def visitEventGUI(event):
    if event is None:
        return
    else:
        s = get()
        isNaVisitedChanged = s.updateVisited('naVisited', event.getID())
        if event.isAvailable()[0]:
            isVisitedChanged = s.updateVisited('visited', event.getID())
        else:
            isVisitedChanged = False
        if isNaVisitedChanged or isVisitedChanged:
            s.save()
            g_eventBus.handleEvent(events.LobbySimpleEvent(events.LobbySimpleEvent.EVENTS_UPDATED))
        return


def visitEventsGUI(events):
    """ Mark given events as viewed.
    """
    for event in events:
        visitEventGUI(event)


def expandGroup(groupID, isExpanded):
    if groupID is None:
        return
    else:
        s = get()
        s.updateExpanded(groupID, isExpanded)
        s.save()
        return


def updateCommonEventsSettings(svrEvents):
    s = get()
    s.removeCompleted(set((e.getID() for e in svrEvents.itervalues() if e.isCompleted())))
    s.save()


def _updatePMSettings(**kwargs):
    settings = get()
    settings.personalMissions.update(**kwargs)
    settings.save()


def markPQIntroAsShown():
    _updatePMSettings(introShown=_LAST_PQ_INTRO_VERSION)


def isPMOperationNew(operationID, pmSettings = None):
    pqSettings = pmSettings or get()
    return operationID not in pqSettings.personalMissions.operationsVisited


def isNeedToShowHeaderAlert():
    return get().personalMissions.headerAlert


def markHeaderAlertAsVisited():
    _updatePMSettings(headerAlert=True)