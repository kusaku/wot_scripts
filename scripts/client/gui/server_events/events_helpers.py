# Embedded file name: scripts/client/gui/server_events/events_helpers.py
import time
from collections import namedtuple
from functools import partial
import BigWorld
from adisp import async
from constants import EVENT_TYPE
from gui import makeHtmlString
from gui.Scaleform.genConsts.MISSIONS_STATES import MISSIONS_STATES
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.QUESTS import QUESTS
from gui.server_events import formatters
from gui.shared.gui_items import Vehicle
from gui.shared.gui_items.processors import quests as quests_proc
from gui.shared.utils.decorators import process
from helpers import time_utils, i18n, dependency
from shared_utils import CONST_CONTAINER
from skeletons.gui.server_events import IEventsCache
FINISH_TIME_LEFT_TO_SHOW = time_utils.ONE_DAY
START_TIME_LIMIT = 5 * time_utils.ONE_DAY
AWARDS_PER_PAGE = 3
AWARDS_PER_SINGLE_PAGE = 5

class EventInfoModel(object):
    NO_BONUS_COUNT = -1

    def __init__(self, event):
        self.event = event

    def getTimerMsg(self, key = None):
        startTimeLeft = self.event.getStartTimeLeft()
        if startTimeLeft > 0:
            if startTimeLeft > START_TIME_LIMIT:
                fmt = self._getDateTimeString(self.event.getStartTime())
            else:
                fmt = self._getTillTimeString(startTimeLeft)
            return makeHtmlString('html_templates:lobby/quests', 'timerTillStart', {'time': fmt})
        if FINISH_TIME_LEFT_TO_SHOW > self.event.getFinishTimeLeft() > 0:
            gmtime = time.gmtime(self.event.getFinishTimeLeft())
            if gmtime.tm_hour > 0:
                fmt = i18n.makeString('#quests:item/timer/tillFinish/onlyHours')
            else:
                fmt = i18n.makeString('#quests:item/timer/tillFinish/lessThanHour')
            fmt %= {'hours': time.strftime('%H', gmtime),
             'min': time.strftime('%M', gmtime),
             'days': str(gmtime.tm_mday)}
            return makeHtmlString('html_templates:lobby/quests', 'timerTillFinish', {'time': fmt})
        return ''

    def _getStatus(self, pCur = None):
        return (MISSIONS_STATES.NONE, '')

    @classmethod
    def _getTillTimeString(cls, timeValue):
        return time_utils.getTillTimeString(timeValue, MENU.TIME_TIMEVALUE)

    @classmethod
    def _getDailyProgressResetTimeOffset(cls):
        regionalSettings = BigWorld.player().serverSettings['regional_settings']
        if 'starting_time_of_a_new_game_day' in regionalSettings:
            newDayOffset = regionalSettings['starting_time_of_a_new_game_day']
        elif 'starting_time_of_a_new_day' in regionalSettings:
            newDayOffset = regionalSettings['starting_time_of_a_new_day']
        else:
            newDayOffset = 0
        return newDayOffset

    def _getActiveDateTimeString(self):
        i18nKey, args = None, {}
        if self.event.getFinishTimeLeft() <= time_utils.ONE_DAY:
            gmtime = time.gmtime(self.event.getFinishTimeLeft())
            if gmtime.tm_hour > 0:
                fmt = i18n.makeString(QUESTS.ITEM_TIMER_TILLFINISH_LONGFULLFORMAT)
            else:
                fmt = i18n.makeString(QUESTS.ITEM_TIMER_TILLFINISH_SHORTFULLFORMAT)
            fmt %= {'hours': time.strftime('%H', gmtime)}
            return fmt
        if self.event.getStartTimeLeft() > 0:
            i18nKey = '#quests:details/header/activeDuration'
            args = {'startTime': self._getDateTimeString(self.event.getStartTime()),
             'finishTime': self._getDateTimeString(self.event.getFinishTime())}
        elif self.event.getFinishTimeLeft() <= time_utils.HALF_YEAR:
            i18nKey = '#quests:details/header/tillDate'
            args = {'finishTime': self._getDateTimeString(self.event.getFinishTime())}
        weekDays = self.event.getWeekDays()
        intervals = self.event.getActiveTimeIntervals()
        if weekDays or intervals:
            if i18nKey is None:
                i18nKey = '#quests:details/header/schedule'
            if weekDays:
                days = ', '.join([ i18n.makeString('#menu:dateTime/weekDays/full/%d' % idx) for idx in self.event.getWeekDays() ])
                i18nKey += 'Days'
                args['days'] = days
            if intervals:
                times = []
                for low, high in intervals:
                    times.append('%s - %s' % (BigWorld.wg_getShortTimeFormat(low), BigWorld.wg_getShortTimeFormat(high)))

                i18nKey += 'Times'
                times = ', '.join(times)
                args['times'] = times
        if i18nKey is None:
            return
        else:
            return i18n.makeString(i18nKey, **args)

    @classmethod
    def _getDateTimeString(cls, timeValue):
        return '{0:>s} {1:>s}'.format(BigWorld.wg_getLongDateFormat(timeValue), BigWorld.wg_getShortTimeFormat(timeValue))


class QuestInfoModel(EventInfoModel):

    def _getActiveDateTimeString(self):
        timeLeft = self.event.getFinishTimeLeft()
        if timeLeft <= time_utils.THREE_QUARTER_HOUR:
            return formatters.formatYellow(QUESTS.DETAILS_HEADER_COMETOENDINMINUTES, minutes=getMinutesRoundByTime(timeLeft))
        return super(QuestInfoModel, self)._getActiveDateTimeString()

    def getTimerMsg(self, key = 'comeToEndInMinutes'):
        timeLeft = self.event.getFinishTimeLeft()
        if timeLeft <= time_utils.THREE_QUARTER_HOUR:
            return makeHtmlString('html_templates:lobby/quests/', key, {'minutes': getMinutesRoundByTime(timeLeft)})
        return super(QuestInfoModel, self).getTimerMsg()

    def _getDailyResetStatus(self, resetLabelKey, labeFormatter):
        if self.event.bonusCond.isDaily():
            resetHourOffset = (time_utils.ONE_DAY - self._getDailyProgressResetTimeOffset()) / time_utils.ONE_HOUR
            if resetHourOffset >= 0:
                return labeFormatter(resetLabelKey) % {'time': time.strftime(i18n.makeString('#quests:details/conditions/postBattle/dailyReset/timeFmt'), time_utils.getTimeStructInLocal(time_utils.getTimeTodayForUTC(hour=resetHourOffset)))}
        return ''

    def _getCompleteDailyStatus(self, completeKey):
        return i18n.makeString(completeKey, time=self._getTillTimeString(time_utils.ONE_DAY - time_utils.getServerRegionalTimeCurrentDay()))


class EVENT_STATUS(CONST_CONTAINER):
    COMPLETED = 'done'
    NOT_AVAILABLE = 'notAvailable'
    WRONG_TIME = 'wrongTime'
    NONE = ''


def getMinutesRoundByTime(timeLeft):
    timeLeft = int(timeLeft)
    return (timeLeft / time_utils.QUARTER_HOUR + cmp(timeLeft % time_utils.QUARTER_HOUR, 0)) * time_utils.QUARTER


def missionsSortFunc(a, b):
    """ Sort function for common quests (all except personal mission and motive).
    """
    res = cmp(a.isAvailable()[0] and not a.isCompleted(), b.isAvailable()[0] and not b.isCompleted())
    if res:
        return res
    res = cmp(a.getPriority(), b.getPriority())
    if res:
        return res
    res = cmp(a.isAvailable()[1] == 'requirement', b.isAvailable()[1] == 'requirement')
    if res:
        return res
    res = cmp(bool(a.isAvailable()[1]), bool(b.isAvailable()[1]))
    if res:
        return res
    res = cmp(a.isCompleted(), b.isCompleted())
    if res:
        return res
    return cmp(a.getUserName(), b.getUserName())


def getConditionsDiffStructure(fullConditions, mainConditions):
    """
    Return conditions diff structure between fullConditions and mainConditions sections with parent tags
    Diff doesn't contain unique mainConditions sections.
    
    example:
    fullConditions: ((win, 1), (and, [(survive, 5), (kill, 3)])
    mainConditions: ((win, 1), (and, [(kill, 3), (damage, 3)])
    result: (and, [(survive, 5)])
    """
    result = []
    if fullConditions == mainConditions:
        return result
    if len(fullConditions) == len(mainConditions):
        for fKey, fValue in fullConditions:
            if (fKey, fValue) not in mainConditions:
                for mKey, mValue in mainConditions:
                    if (mKey, mValue) not in fullConditions:
                        if fKey == mKey:
                            if fValue != mValue:
                                diffValue = getConditionsDiffStructure(fValue, mValue)
                                if diffValue and (fKey, diffValue) not in result:
                                    result.append((fKey, diffValue))
                        elif (fKey, fValue) not in result:
                            result.append((fKey, fValue))

        return result
    for fValue in fullConditions:
        if fValue not in mainConditions:
            result.append(fValue)

    return result


class _PMDependenciesResolver(object):
    eventsCache = dependency.descriptor(IEventsCache)
    _DEPENDENCIES_LIST = namedtuple('HandlersList', ['cache',
     'progress',
     'selectProcessor',
     'refuseProcessor',
     'rewardsProcessor',
     'pawnProcessor',
     'sorter'])

    @classmethod
    def _makeRandomDependencies(cls):
        return cls._DEPENDENCIES_LIST(cls.eventsCache.random, cls.eventsCache.randomQuestsProgress, quests_proc.RandomQuestSelect, quests_proc.RandomQuestRefuse, quests_proc.PersonalMissionsGetRegularReward, quests_proc.PersonalMissionPawn, partial(sorted, cmp=Vehicle.compareByVehTypeName))

    @classmethod
    def chooseList(cls, _):
        return cls._makeRandomDependencies()


def getPersonalMissionsCache(questsType = None):
    return _PMDependenciesResolver.chooseList(questsType).cache


def getPersonalMissionsProgress(questsType = None):
    return _PMDependenciesResolver.chooseList(questsType).progress


def getPersonalMissionsSelectProcessor(questsType = None):
    return _PMDependenciesResolver.chooseList(questsType).selectProcessor


def getPersonalMissionsRefuseProcessor(questsType = None):
    return _PMDependenciesResolver.chooseList(questsType).refuseProcessor


def getPersonalMissionsRewardProcessor(questsType = None):
    return _PMDependenciesResolver.chooseList(questsType).rewardsProcessor


def getPersonalMissionsPawnProcessor(questsType = None):
    return _PMDependenciesResolver.chooseList(questsType).pawnProcessor


def sortWithQuestType(items, key, questsType = None):
    return _PMDependenciesResolver.chooseList(questsType).sorter(items, key=key)


@async
@process('updating')
def getPersonalMissionAward(quest, callback):
    """ Display special tankwoman award window.
    """
    from gui.server_events.events_dispatcher import showTankwomanAward
    tankman, isMainBonus = quest.getTankmanBonus()
    needToGetTankman = quest.needToGetAddReward() and not isMainBonus or quest.needToGetMainReward() and isMainBonus
    if needToGetTankman and tankman is not None:
        for tmanData in tankman.getTankmenData():
            showTankwomanAward(quest.getID(), tmanData)
            break

        result = None
    else:
        result = yield getPersonalMissionsRewardProcessor()(quest).request()
    callback(result)
    return


def questsSortFunc(a, b):
    """ Sort function for common quests (all except personal missions and motive).
    """
    res = cmp(a.isCompleted(), b.isCompleted())
    if res:
        return res
    res = cmp(a.getPriority(), b.getPriority())
    if res:
        return res
    return cmp(a.getUserName(), b.getUserName())


def getBoosterQuests():

    def filterQuests(quest):
        hasBooster = len(quest.getBonuses('goodies'))
        isNotRanked = quest.getType() != EVENT_TYPE.RANKED_QUEST
        return hasBooster and isNotRanked and quest.isAvailable()[0] and not quest.isCompleted()

    eventsCache = dependency.instance(IEventsCache)
    return eventsCache.getActiveQuests(filterFunc=filterQuests)