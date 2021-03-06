# Embedded file name: scripts/client/gui/game_control/AwardController.py
import types
import weakref
from abc import ABCMeta, abstractmethod
from collections import defaultdict
import BigWorld
import ArenaType
import gui.awards.event_dispatcher as shared_events
import personal_missions
from PlayerEvents import g_playerEvents
from account_helpers.AccountSettings import AccountSettings, AWARDS
from account_shared import getFairPlayViolationName
from chat_shared import SYS_MESSAGE_TYPE
from constants import EVENT_TYPE, INVOICE_ASSET
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_WARNING, LOG_ERROR, LOG_DEBUG
from dossiers2.custom.records import DB_ID_TO_RECORD
from dossiers2.ui.layouts import PERSONAL_MISSIONS_GROUP
from gui import SystemMessages
from gui import DialogsInterface
from gui.ClientUpdateManager import g_clientUpdateManager
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.dialogs import I18PunishmentDialogMeta
from gui.Scaleform.genConsts.RANKEDBATTLES_ALIASES import RANKEDBATTLES_ALIASES
from gui.Scaleform.locale.DIALOGS import DIALOGS
from gui.Scaleform.locale.SYSTEM_MESSAGES import SYSTEM_MESSAGES
from gui.gold_fish import isGoldFishActionActive, isTimeToShowGoldFishPromo
from gui.prb_control.entities.listener import IGlobalListener
from gui.prb_control.settings import BATTLES_TO_SELECT_RANDOM_MIN_LIMIT
from gui.ranked_battles import ranked_helpers
from gui.server_events import events_dispatcher as quests_events
from gui.shared import EVENT_BUS_SCOPE, g_eventBus, events
from gui.shared.gui_items.Tankman import Tankman
from gui.shared.gui_items.Vehicle import Vehicle
from gui.shared.gui_items.dossier.factories import getAchievementFactory
from gui.shared.utils import isPopupsWindowsOpenDisabled
from gui.shared.utils.requesters import REQ_CRITERIA
from gui.shared.utils.transport import z_loads
from helpers import dependency
from helpers import i18n
from items import ITEM_TYPE_INDICES, getTypeOfCompactDescr, vehicles as vehicles_core
from messenger.formatters import NCContextItemFormatter, TimeFormatter
from messenger.formatters.service_channel import TelecomReceivedInvoiceFormatter
from messenger.proto.events import g_messengerEvents
from skeletons.gui.game_control import IRefSystemController, IAwardController, IRankedBattlesController, IBootcampController
from skeletons.gui.goodies import IGoodiesCache
from skeletons.gui.server_events import IEventsCache
from skeletons.gui.shared import IItemsCache
from skeletons.new_year import INewYearController
from gui.shared.utils.functions import getViewName
from items.new_year_types import NY_STATE

class AwardController(IAwardController, IGlobalListener):
    refSystem = dependency.descriptor(IRefSystemController)
    bootcampController = dependency.descriptor(IBootcampController)
    eventsCache = dependency.descriptor(IEventsCache)

    def __init__(self):
        self.__handlers = [BattleQuestsAutoWindowHandler(self),
         QuestBoosterAwardHandler(self),
         BoosterAfterBattleAwardHandler(self),
         PunishWindowHandler(self),
         RefSystemQuestsWindowHandler(self),
         PersonalMissionsBonusHandler(self),
         PMWindowAfterBattleHandler(self),
         TokenQuestsWindowHandler(self),
         MotiveQuestsWindowHandler(self),
         RefSysStatusWindowHandler(self),
         VehiclesResearchHandler(self),
         VictoryHandler(self),
         BattlesCountHandler(self),
         PveBattlesCountHandler(self),
         PersonalMissionsAutoWindowHandler(self),
         PersonalMissionByAwardListHandler(self),
         PersonalMissionOperationAwardHandler(self),
         PersonalMissionOperationUnlockedHandler(self),
         GoldFishHandler(self),
         TelecomHandler(self),
         RankedQuestsHandler(self),
         MarkByInvoiceHandler(self),
         MarkByQuestHandler(self),
         _NYBoxesHandler(self)]
        super(AwardController, self).__init__()
        self.__delayedHandlers = []
        self.__isLobbyLoaded = False

    def init(self):
        for handler in self.__handlers:
            handler.init()

    def fini(self):
        for handler in self.__handlers:
            handler.fini()

    def postponeOrCall(self, handler, ctx):
        if self.canShow():
            handler(ctx)
        else:
            LOG_DEBUG('Postponed award call:', handler, ctx)
            self.__delayedHandlers.append((handler, ctx))

    def handlePostponed(self, *args):
        if self.canShow():
            for handler, ctx in self.__delayedHandlers:
                LOG_DEBUG('Calling postponed award handler:', handler, ctx)
                handler(ctx)

            self.__delayedHandlers = []

    def canShow(self):
        popupsWindowsDisabled = isPopupsWindowsOpenDisabled() or self.bootcampController.isInBootcamp()
        prbDispatcher = self.prbDispatcher
        if prbDispatcher is None:
            return self.__isLobbyLoaded and not popupsWindowsDisabled
        else:
            return self.__isLobbyLoaded and not popupsWindowsDisabled and not prbDispatcher.getFunctionalState().hasLockedState

    def onAvatarBecomePlayer(self):
        self.__isLobbyLoaded = False
        self.stopGlobalListening()

    def onDisconnected(self):
        self.__isLobbyLoaded = False
        self.stopGlobalListening()
        for handler in self.__handlers:
            handler.stop()

    def onLobbyInited(self, *args):
        self.startGlobalListening()
        self.__isLobbyLoaded = True
        self.handlePostponed()
        for handler in self.__handlers:
            handler.start()

    def onPlayerStateChanged(self, entity, roster, accountInfo):
        self.handlePostponed()

    def onUnitFlagsChanged(self, flags, timeLeft):
        self.handlePostponed()

    def onDequeued(self, queueType, *args):
        self.handlePostponed()


class AwardHandler(object):
    __metaclass__ = ABCMeta
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self, awardCtrl):
        self._awardCtrl = weakref.proxy(awardCtrl)

    def init(self):
        pass

    def fini(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def handle(self, *args):
        if self._needToShowAward(args):
            self._awardCtrl.postponeOrCall(self._showAward, args)

    def isShowCongrats(self, quest):
        if quest:
            return quest.getData().get('showCongrats', False)
        return False

    @abstractmethod
    def _needToShowAward(self, ctx):
        pass

    @abstractmethod
    def _showAward(self, ctx):
        pass


class ServiceChannelHandler(AwardHandler):
    eventsCache = dependency.descriptor(IEventsCache)

    def __init__(self, type, awardCtrl):
        super(ServiceChannelHandler, self).__init__(awardCtrl)
        self.__type = type

    def init(self):
        g_messengerEvents.serviceChannel.onChatMessageReceived += self.handle

    def fini(self):
        g_messengerEvents.serviceChannel.onChatMessageReceived -= self.handle

    def _needToShowAward(self, ctx):
        _, message = ctx
        return message is not None and message.type == self.__type and message.data is not None


class PunishWindowHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(PunishWindowHandler, self).__init__(SYS_MESSAGE_TYPE.battleResults.index(), awardCtrl)

    def _showAward(self, ctx):
        _, message = ctx
        arenaTypeID = message.data.get('arenaTypeID', 0)
        if arenaTypeID > 0 and arenaTypeID in ArenaType.g_cache:
            arenaType = ArenaType.g_cache[arenaTypeID]
        else:
            arenaType = None
        arenaCreateTime = message.data.get('arenaCreateTime', None)
        fairplayViolations = message.data.get('fairplayViolations', None)
        if arenaCreateTime and arenaType and fairplayViolations is not None and fairplayViolations[:2] != (0, 0):
            penaltyType = None
            violation = None
            if fairplayViolations[1] != 0:
                penaltyType = 'penalty'
                violation = fairplayViolations[1]
            elif fairplayViolations[0] != 0:
                penaltyType = 'warning'
                violation = fairplayViolations[0]
            from gui.DialogsInterface import showDialog
            showDialog(I18PunishmentDialogMeta('punishmentWindow', None, {'penaltyType': penaltyType,
             'arenaName': i18n.makeString(arenaType.name),
             'time': TimeFormatter.getActualMsgTimeStr(arenaCreateTime),
             'reason': i18n.makeString(DIALOGS.all('punishmentWindow/reason/%s' % getFairPlayViolationName(violation)))}), lambda *args: None)
        return


class RefSystemQuestsWindowHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(RefSystemQuestsWindowHandler, self).__init__(SYS_MESSAGE_TYPE.refSystemQuests.index(), awardCtrl)

    def _showAward(self, ctx):
        _, message = ctx
        completedQuestIDs = message.data.get('completedQuestIDs', set())
        for tmanCompDescr in message.data.get('tankmen') or []:
            self._awardCtrl.refSystem.showTankmanAwardWindow(Tankman(tmanCompDescr), completedQuestIDs)

        for vehiclesData in message.data.get('vehicles', []):
            for vehTypeCompDescr in vehiclesData:
                self._awardCtrl.refSystem.showVehicleAwardWindow(Vehicle(typeCompDescr=abs(vehTypeCompDescr)), completedQuestIDs)

        self._awardCtrl.refSystem.showCreditsAwardWindow(message.data.get('credits', 0), completedQuestIDs)


class PersonalMissionsBonusHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(PersonalMissionsBonusHandler, self).__init__(SYS_MESSAGE_TYPE.potapovQuestBonus.index(), awardCtrl)

    def _showAward(self, ctx):
        LOG_DEBUG('Show personal mission bonus award!', ctx)
        data = ctx[1].data
        achievements = []
        for recordIdx, value in data.get('popUpRecords', []):
            factory = getAchievementFactory(DB_ID_TO_RECORD[recordIdx])
            if factory is not None:
                a = factory.create(value=int(value))
                if a is not None:
                    achievements.append(a)

        if achievements:
            quests_events.showAchievementsAward(achievements)
        return


class PMWindowAfterBattleHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(PMWindowAfterBattleHandler, self).__init__(SYS_MESSAGE_TYPE.battleResults.index(), awardCtrl)

    def _showAward(self, ctx):
        achievements = []
        popUpRecords = ctx[1].data.get('popUpRecords', [])
        for recordIdx, value in popUpRecords:
            recordName = DB_ID_TO_RECORD[recordIdx]
            if recordName in PERSONAL_MISSIONS_GROUP:
                factory = getAchievementFactory(recordName)
                if factory is not None:
                    a = factory.create(value=int(value))
                    if a is not None:
                        achievements.append(a)

        if achievements:
            quests_events.showAchievementsAward(achievements)
        return


class TokenQuestsWindowHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(TokenQuestsWindowHandler, self).__init__(SYS_MESSAGE_TYPE.tokenQuests.index(), awardCtrl)

    def _showAward(self, ctx):
        data = ctx[1].data
        completedQuests = {}
        completedQuestIDs = data.get('completedQuestIDs', set())
        filterCompleted = lambda q: q.getID() in completedQuestIDs
        allCompletedQuests = self.eventsCache.getAllQuests(includePersonalMissions=True, filterFunc=filterCompleted)
        for quest in allCompletedQuests.itervalues():
            if self.isShowCongrats(quest):
                completedQuests[quest.getID()] = (quest, {'eventsCache': self.eventsCache})

        for quest, context in completedQuests.itervalues():
            self._showWindow(quest, context)

    @staticmethod
    def _showWindow(quest, context):
        """Fire an actual show event to display an award window.
        
        :param quest: instance of event_items.Quest (or derived)
        :param context: dict with required data
        """
        quests_events.showMissionAward(quest, context)


class MarkByInvoiceHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(MarkByInvoiceHandler, self).__init__(SYS_MESSAGE_TYPE.invoiceReceived.index(), awardCtrl)

    def _showAward(self, ctx):
        invoiceData = ctx[1].data
        if 'assetType' in invoiceData and invoiceData['assetType'] == INVOICE_ASSET.DATA:
            if 'data' in invoiceData:
                data = invoiceData['data']
                if 'tokens' in data:
                    tokensDict = data['tokens']
                    for tokenName, tokenData in tokensDict.iteritems():
                        if tokenName.startswith('img:'):
                            count = tokenData.get('count', 0)
                            if count:
                                self._showWindow(count)

    @staticmethod
    def _showWindow(tokenCount):
        SystemMessages.pushI18nMessage(SYSTEM_MESSAGES.TOKENS_NOTIFICATION_MARK_ACQUIRED, count=tokenCount, type=SystemMessages.SM_TYPE.tokenWithMarkAcquired)


class MarkByQuestHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(MarkByQuestHandler, self).__init__(SYS_MESSAGE_TYPE.battleResults.index(), awardCtrl)
        self.__questTypes = [SYS_MESSAGE_TYPE.battleResults.index(), SYS_MESSAGE_TYPE.tokenQuests.index()]

    def _needToShowAward(self, ctx):
        _, message = ctx
        return message is not None and message.type in self.__questTypes and message.data is not None

    def _showAward(self, ctx):
        messageData = ctx[1].data
        if 'tokens' in messageData:
            tokensDict = messageData['tokens']
            for tokenName, tokenData in tokensDict.iteritems():
                if tokenName.startswith('img:'):
                    count = tokenData.get('count', 0)
                    if count:
                        self._showWindow(count)

    @staticmethod
    def _showWindow(tokenCount):
        SystemMessages.pushI18nMessage(SYSTEM_MESSAGES.TOKENS_NOTIFICATION_MARK_ACQUIRED, count=tokenCount, type=SystemMessages.SM_TYPE.tokenWithMarkAcquired)


class MotiveQuestsWindowHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(MotiveQuestsWindowHandler, self).__init__(SYS_MESSAGE_TYPE.battleResults.index(), awardCtrl)

    def _showAward(self, ctx):
        data = ctx[1].data
        motiveQuests = self.eventsCache.getMotiveQuests()
        for qID in data.get('completedQuestIDs', set()):
            if qID in motiveQuests and self.isShowCongrats(motiveQuests[qID]):
                quests_events.showMotiveAward(motiveQuests[qID])


class QuestBoosterAwardHandler(ServiceChannelHandler):
    goodiesCache = dependency.descriptor(IGoodiesCache)

    def __init__(self, awardCtrl):
        super(QuestBoosterAwardHandler, self).__init__(SYS_MESSAGE_TYPE.tokenQuests.index(), awardCtrl)

    def _showAward(self, ctx):
        data = ctx[1].data
        goodies = data.get('goodies', {})
        for boosterID in goodies:
            booster = self.goodiesCache.getBooster(boosterID)
            if booster is not None and booster.enabled:
                shared_events.showBoosterAward(booster)

        return


class BoosterAfterBattleAwardHandler(ServiceChannelHandler):
    goodiesCache = dependency.descriptor(IGoodiesCache)

    def __init__(self, awardCtrl):
        super(BoosterAfterBattleAwardHandler, self).__init__(SYS_MESSAGE_TYPE.battleResults.index(), awardCtrl)

    def _showAward(self, ctx):
        goodies = ctx[1].data.get('goodies', {})
        for boosterID in goodies:
            booster = self.goodiesCache.getBooster(boosterID)
            if booster is not None and booster.enabled:
                shared_events.showBoosterAward(booster)

        return


class BattleQuestsAutoWindowHandler(ServiceChannelHandler):
    """ Handler responsible for battle quests awards.
    """

    def __init__(self, awardCtrl):
        super(BattleQuestsAutoWindowHandler, self).__init__(SYS_MESSAGE_TYPE.battleResults.index(), awardCtrl)

    def _showAward(self, ctx):
        _, message = ctx
        completedQuests = {}
        allQuests = self.eventsCache.getAllQuests(includePersonalMissions=True, filterFunc=lambda quest: self._isAppropriate(quest))
        completedQuestUniqueIDs = message.data.get('completedQuestIDs', set())
        for uniqueQuestID in completedQuestUniqueIDs:
            questID, ctx = self._getContext(uniqueQuestID, completedQuests, completedQuestUniqueIDs)
            if questID in allQuests:
                quest = allQuests[questID]
                if self.isShowCongrats(quest):
                    ctx.update(eventsCache=self.eventsCache)
                    completedQuests[questID] = (quest, ctx)

        for quest, context in completedQuests.itervalues():
            self._showWindow(quest, context)

    @staticmethod
    def _showWindow(quest, context):
        """Fire an actual show event to display an award window.
        
        :param quest: instance of event_items.Quest (or derived)
        :param context: dict with required data
        """
        quests_events.showMissionAward(quest, context)

    @staticmethod
    def _isAppropriate(quest):
        """ Check if quest is appropriate for the current handler's scope.
        
        :param quest: instance of event_items.Quest (or derived)
        """
        return quest.getType() in (EVENT_TYPE.BATTLE_QUEST,
         EVENT_TYPE.TOKEN_QUEST,
         EVENT_TYPE.PERSONAL_QUEST,
         EVENT_TYPE.RANKED_QUEST)

    @staticmethod
    def _getContext(uniqueQuestID, completedQuests, completedQuestUniqueIDs):
        """ Gather the data needed by award window and get real quest id.
        
        :param uniqueQuestID: unique id of the quest (considering its sub quests)
        :param completedQuests: dict {questID: (quest, context)}
        :param completedQuestUniqueIDs: list with ids of completed quests
        
        :return: tuple (quest id, context)
        """
        return (uniqueQuestID, {})


class PersonalMissionsAutoWindowHandler(BattleQuestsAutoWindowHandler):
    """ Handler responsible for personal quests awards.
    """

    @staticmethod
    def _showWindow(quest, context):
        quests_events.showPersonalMissionAward(quest, context)

    @staticmethod
    def _isAppropriate(quest):
        return quest.getType() == EVENT_TYPE.PERSONAL_MISSION

    @staticmethod
    def _getContext(uniqueQuestID, completedQuests, completedQuestUniqueIDs):
        if personal_missions.g_cache.isPersonalMission(uniqueQuestID):
            pqType = personal_missions.g_cache.questByUniqueQuestID(uniqueQuestID)
            if pqType.id not in completedQuests:
                ctx = {'isMainReward': pqType.mainQuestID in completedQuestUniqueIDs,
                 'isAddReward': pqType.addQuestID in completedQuestUniqueIDs}
                return (pqType.id, ctx)
        return (None, {})


class PersonalMissionByAwardListHandler(PersonalMissionsAutoWindowHandler):
    """Personal Mission completed by pawned award list
    """

    def _needToShowAward(self, ctx):
        _, msg = ctx
        if msg is not None and isinstance(msg.data, types.DictType):
            completedQuestUniqueIDs = msg.data.get('completedQuestIDs', set())
            for uniqueQuestID in completedQuestUniqueIDs:
                if personal_missions.g_cache.isPersonalMission(uniqueQuestID) and uniqueQuestID.endswith('_main_award_list'):
                    return True

        return False

    @staticmethod
    def _showWindow(quest, context):
        quests_events.showPersonalMissionAward(quest, context)

    @staticmethod
    def _getContext(uniqueQuestID, completedQuests, completedQuestUniqueIDs):
        if personal_missions.g_cache.isPersonalMission(uniqueQuestID):
            pqType = personal_missions.g_cache.questByUniqueQuestID(uniqueQuestID)
            if pqType.id not in completedQuests:
                ctx = {'isMainReward': True,
                 'isAddReward': False}
                return (pqType.id, ctx)
        return (None, {})


class PersonalMissionOperationAwardHandler(BattleQuestsAutoWindowHandler):
    """operation complete, show congrats and next operations views
    """
    OPERATION_PREFIXES = {'pt_final_s1_t1': 1,
     'pt_final_s1_t2': 2,
     'pt_final_s1_t3': 3,
     'pt_final_s1_t4': 4}
    BADGE_QUEST_ID = 'pt_final_badge'
    ATTACH_TO_OPERATION = 4

    def _needToShowAward(self, ctx):
        _, msg = ctx
        if msg is not None and isinstance(msg.data, types.DictType):
            completedQuestUniqueIDs = msg.data.get('completedQuestIDs', set())
            for uniqueQuestID in completedQuestUniqueIDs:
                if uniqueQuestID == self.BADGE_QUEST_ID:
                    return True
                for operationToken in self.OPERATION_PREFIXES:
                    if uniqueQuestID.startswith(operationToken):
                        return True

        return False

    def _showAward(self, ctx):
        _, message = ctx
        completedQuests = defaultdict(dict)
        allQuests = self.eventsCache.getHiddenQuests()
        completedQuestUniqueIDs = message.data.get('completedQuestIDs', set())
        for uniqueQuestID in (qID for qID in completedQuestUniqueIDs if qID in allQuests):
            if uniqueQuestID == self.BADGE_QUEST_ID:
                quest = allQuests[uniqueQuestID]
                completedQuests[self.ATTACH_TO_OPERATION][uniqueQuestID] = quest
            else:
                for oRewardPrefix, oID in self.OPERATION_PREFIXES.iteritems():
                    if uniqueQuestID.startswith(oRewardPrefix):
                        quest = allQuests[uniqueQuestID]
                        completedQuests[oID][uniqueQuestID] = quest

        for operationID, quests in completedQuests.iteritems():
            ctx = {'operationID': operationID,
             'quests': quests}
            self._showWindow(None, ctx)

        return

    @staticmethod
    def _showWindow(quest, context):
        quests_events.showPersonalMissionCongratulationAward(context)


class PersonalMissionOperationUnlockedHandler(BattleQuestsAutoWindowHandler):
    """operation complete, show next operations views
    """
    OPERATION_COMPLETION_IDS = {'pt_final_s1_t1': 1,
     'pt_final_s1_t2': 2,
     'pt_final_s1_t3': 3,
     'pt_final_s1_t4': 4}

    def _needToShowAward(self, ctx):
        _, msg = ctx
        if msg is not None and isinstance(msg.data, types.DictType):
            completedQuestUniqueIDs = msg.data.get('completedQuestIDs', set())
            for uniqueQuestID in completedQuestUniqueIDs:
                if uniqueQuestID in self.OPERATION_COMPLETION_IDS:
                    return True

        return False

    def _showAward(self, ctx):
        _, message = ctx
        allQuests = self.eventsCache.getHiddenQuests()
        operations = self.eventsCache.personalMissions.getOperations()
        context = {'eventsCache': self.eventsCache}
        completedQuestUniqueIDs = message.data.get('completedQuestIDs', set())
        for uniqueQuestID in (qID for qID in completedQuestUniqueIDs if qID in allQuests):
            for oCompletionID, oID in self.OPERATION_COMPLETION_IDS.iteritems():
                if uniqueQuestID == oCompletionID:
                    quest = allQuests[uniqueQuestID]
                    operation = operations[oID]
                    nextOperationID = operation.getNextOperationID()
                    if nextOperationID:
                        context['nextOperationID'] = nextOperationID
                        self._showWindow(quest, context)

    @staticmethod
    def _showWindow(quest, context):
        quests_events.showOperationUnlockedAward(quest, context)


class RefSysStatusWindowHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(RefSysStatusWindowHandler, self).__init__(SYS_MESSAGE_TYPE.notificationsCenter.index(), awardCtrl)

    def _showAward(self, ctx):
        data = z_loads(ctx[1].data)
        if 'window' not in data:
            return
        context = {}
        if 'context' in data:
            context = self.__formatContext(data['context'])
        if data['window'] == 1:
            self.__showRefSystemNotification('showReferrerIntroWindow', invitesCount=context.get('invites_count', 0))
        elif data['window'] == 2:
            self.__showRefSystemNotification('showReferralIntroWindow', nickname=context['nickname'], isNewbie=True)
        elif data['window'] == 3:
            self.__showRefSystemNotification('showReferralIntroWindow', nickname=context['nickname'], isNewbie=False)
        else:
            LOG_WARNING('Unknown referral system user status window', data)

    def __showRefSystemNotification(self, methodName, **ctx):
        try:
            getattr(self._awardCtrl.refSystem, methodName)(**ctx)
        except:
            LOG_ERROR('There is exception while processing notification center window', methodName, ctx)
            LOG_CURRENT_EXCEPTION()

    def __formatContext(self, ctx):
        result = {}
        if type(ctx) is not types.DictType:
            LOG_ERROR('Context is invalid', ctx)
            return result
        getItemFormat = NCContextItemFormatter.getItemFormat
        for key, item in ctx.iteritems():
            if len(item) > 1:
                itemType, itemValue = item[0:2]
                result[key] = getItemFormat(itemType, itemValue)
            else:
                LOG_ERROR('Context item is invalid', item)
                result[key] = str(item)

        return result


class SpecialAchievement(AwardHandler):
    bootcampController = dependency.descriptor(IBootcampController)

    def __init__(self, key, awardCtrl, awardCountToMessage):
        super(SpecialAchievement, self).__init__(awardCtrl)
        self.__key = key
        self._awardCntToMsg = awardCountToMessage

    def isChanged(self, value):
        return value != AccountSettings.getFilter(AWARDS).get(self.__key)

    def getAchievementCount(self):
        raise NotImplementedError

    def showAwardWindow(self, achievementCount, messageNumber):
        raise NotImplementedError

    def _needToShowAward(self, ctx = None):
        return (not self._awardCtrl.canShow() or self._getAchievementToShow() is not None) and not self.bootcampController.isInBootcamp()

    def _getAchievementToShow(self):
        achievementCount = self.getAchievementCount()
        lastElement = max(self._awardCntToMsg.keys())
        if achievementCount != 0 and self.isChanged(achievementCount):
            if achievementCount in self._awardCntToMsg or achievementCount % lastElement == 0:
                return achievementCount
            sortedKeys = sorted(self._awardCntToMsg.keys(), reverse=True)
            for i in xrange(len(sortedKeys) - 1):
                if sortedKeys[i] > achievementCount and achievementCount > sortedKeys[i + 1] and self.isChanged(sortedKeys[i + 1]):
                    return sortedKeys[i + 1]

        return None

    def _showAward(self, ctx = None):
        achievementCount = self._getAchievementToShow()
        if achievementCount is not None:
            messageNumber = self._awardCntToMsg.get(achievementCount, self._awardCntToMsg[max(self._awardCntToMsg.keys())])
            self.__setNewValue(achievementCount)
            self.showAwardWindow(achievementCount, messageNumber)
        return

    def __setNewValue(self, value):
        achievement = AccountSettings.getFilter(AWARDS)
        achievement[self.__key] = value
        AccountSettings.setFilter(AWARDS, achievement)


class VehiclesResearchHandler(SpecialAchievement):
    VEHICLE_AMOUNT = {2: 1,
     5: 2,
     10: 3,
     20: 4,
     30: 1}

    def __init__(self, awardCtrl):
        super(VehiclesResearchHandler, self).__init__('vehicleResearchAward', awardCtrl, VehiclesResearchHandler.VEHICLE_AMOUNT)

    def init(self):
        g_clientUpdateManager.addCallbacks({'stats.unlocks': self.onUnlocksChanged})

    def fini(self):
        g_clientUpdateManager.removeObjectCallbacks(self)

    def getAchievementCount(self):
        return len(self.itemsCache.items.getVehicles(criteria=REQ_CRITERIA.UNLOCKED | ~REQ_CRITERIA.SECRET | ~REQ_CRITERIA.VEHICLE.PREMIUM | ~REQ_CRITERIA.VEHICLE.LEVELS([1]) | ~REQ_CRITERIA.VEHICLE.IS_PREMIUM_IGR))

    def onUnlocksChanged(self, unlocks):
        isChanged = False
        for unlock in list(unlocks):
            if getTypeOfCompactDescr(unlock) == ITEM_TYPE_INDICES['vehicle']:
                isChanged = True

        if isChanged:
            self.handle()

    def showAwardWindow(self, achievementCount, messageNumber):
        return shared_events.showResearchAward(achievementCount, messageNumber)


class VictoryHandler(SpecialAchievement):
    VICTORY_AMOUNT = {5: 1,
     10: 2,
     20: 3,
     50: 4,
     100: 1,
     250: 2,
     500: 3,
     1000: 4}

    def __init__(self, awardCtrl):
        super(VictoryHandler, self).__init__('victoryAward', awardCtrl, VictoryHandler.VICTORY_AMOUNT)

    def init(self):
        g_playerEvents.onGuiCacheSyncCompleted += self.handle
        g_playerEvents.onDossiersResync += self.handle
        g_playerEvents.onBattleResultsReceived += self.handle

    def fini(self):
        g_playerEvents.onGuiCacheSyncCompleted -= self.handle
        g_playerEvents.onDossiersResync -= self.handle
        g_playerEvents.onBattleResultsReceived -= self.handle

    def getAchievementCount(self):
        return self.itemsCache.items.getAccountDossier().getTotalStats().getWinsCount()

    def showAwardWindow(self, achievementCount, messageNumber):
        return shared_events.showVictoryAward(achievementCount, messageNumber)


class BattlesCountHandler(SpecialAchievement):
    BATTLE_AMOUNT = {50: 2,
     100: 3,
     250: 4,
     500: 1,
     1000: 2,
     2000: 3,
     5000: 4,
     7500: 1,
     10000: 2}

    def __init__(self, awardCtrl, key = 'battlesCountAward'):
        super(BattlesCountHandler, self).__init__(key, awardCtrl, self._getAwardCountToMessage())

    def init(self):
        g_playerEvents.onGuiCacheSyncCompleted += self.handle
        g_playerEvents.onDossiersResync += self.handle
        g_playerEvents.onBattleResultsReceived += self.handle

    def fini(self):
        g_playerEvents.onGuiCacheSyncCompleted -= self.handle
        g_playerEvents.onDossiersResync -= self.handle
        g_playerEvents.onBattleResultsReceived -= self.handle

    def getAchievementCount(self):
        return self.itemsCache.items.getAccountDossier().getTotalStats().getBattlesCount()

    def showAwardWindow(self, achievementCount, messageNumber):
        return shared_events.showBattleAward(achievementCount, messageNumber)

    def _getAwardCountToMessage(self):
        return BattlesCountHandler.BATTLE_AMOUNT


class PveBattlesCountHandler(BattlesCountHandler):

    def __init__(self, awardCtrl):
        super(PveBattlesCountHandler, self).__init__(awardCtrl, 'pveBattlesCountAward')

    def getAchievementCount(self):
        return self.itemsCache.items.getAccountDossier().getRandomStats().getBattlesCount()

    def showAwardWindow(self, achievementCount, messageNumber):
        return shared_events.showPveBattleAward(achievementCount, messageNumber)

    def _getAwardCountToMessage(self):
        return {BATTLES_TO_SELECT_RANDOM_MIN_LIMIT: 1}

    def _getAchievementToShow(self):
        achievementCount = self.getAchievementCount()
        if achievementCount != 0 and self.isChanged(achievementCount):
            if achievementCount in self._awardCntToMsg:
                return achievementCount
        return None


class GoldFishHandler(AwardHandler):

    def start(self):
        self.handle()

    def _needToShowAward(self, ctx):
        return True

    def _showAward(self, ctx):
        if isGoldFishActionActive() and isTimeToShowGoldFishPromo():
            g_eventBus.handleEvent(events.LoadViewEvent(VIEW_ALIAS.GOLD_FISH_WINDOW), scope=EVENT_BUS_SCOPE.LOBBY)


class TelecomHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl):
        super(TelecomHandler, self).__init__(SYS_MESSAGE_TYPE.telecomOrderCreated.index(), awardCtrl)

    @staticmethod
    def __getVehileDesrs(data):
        return [ vehicles_core.getVehicleType(vehDesr).compactDescr for vehDesr in data['data']['vehicles'] ]

    def _showAward(self, ctx):
        data = ctx[1].data
        hasCrew = TelecomReceivedInvoiceFormatter.invoiceHasCrew(data)
        hasBrotherhood = TelecomReceivedInvoiceFormatter.invoiceHasBrotherhood(data)
        vehicleDesrs = self.__getVehileDesrs(data)
        if vehicleDesrs:
            shared_events.showTelecomAward(vehicleDesrs, hasCrew, hasBrotherhood)
        else:
            LOG_ERROR("Can't show telecom award window!")


class MultiTypeServiceChannelHandler(ServiceChannelHandler):

    def __init__(self, awardCtrl, handledTypes):
        super(MultiTypeServiceChannelHandler, self).__init__(None, awardCtrl)
        self.__types = handledTypes
        return

    def _needToShowAward(self, ctx):
        _, message = ctx
        return message is not None and message.type in self.__types and message.data is not None

    def _showAward(self, ctx):
        pass


class RankedQuestsHandler(MultiTypeServiceChannelHandler):
    rankedController = dependency.descriptor(IRankedBattlesController)

    def __init__(self, awardCtrl):
        super(RankedQuestsHandler, self).__init__(awardCtrl, (SYS_MESSAGE_TYPE.rankedQuests.index(), SYS_MESSAGE_TYPE.tokenQuests.index()))
        self.__pending = []
        self.__locked = False

    def _showAward(self, ctx):
        _, message = ctx
        data = message.data.copy()
        for questID in filter(ranked_helpers.isRankedQuestID, data.pop('completedQuestIDs', [])):
            if message.type == SYS_MESSAGE_TYPE.rankedQuests.index():
                quest = self.eventsCache.getRankedQuests().get(questID)
                if quest:
                    if quest.isProcessedAtCycleEnd():
                        self.__processOrHold(self.__showCycleAward, (quest, data))
                    elif quest.isBooby():
                        self.__processOrHold(self.__showBoobyAwardWindow, (quest,))
            elif message.type == SYS_MESSAGE_TYPE.tokenQuests.index():
                quest = self.eventsCache.getHiddenQuests().get(questID)
                if quest:
                    self.__processOrHold(self.__showSeasonAward, (quest, data))

    def __processOrHold(self, method, args):
        if self.__locked:
            self.__pending.append((method, args))
        else:
            self.__locked = True
            method(*args)

    def __unlock(self):
        self.__locked = False
        if self.__pending:
            self.__processOrHold(*self.__pending.pop(0))

    def __showCycleAward(self, quest, data):
        season = self.rankedController.getSeason(quest.getSeasonID())
        if season is not None:
            g_eventBus.handleEvent(events.LoadViewEvent(RANKEDBATTLES_ALIASES.RANKED_BATTLES_STAGE_COMPLETE, ctx={'quest': quest,
             'awards': data,
             'closeClb': self.__unlock,
             'season': season}), scope=EVENT_BUS_SCOPE.LOBBY)
        else:
            self.__unlock()
        return

    def __showSeasonAward(self, quest, data):
        seasonID, _, _ = ranked_helpers.getRankedDataFromTokenQuestID(quest.getID())
        season = self.rankedController.getSeason(seasonID)
        if season is not None:
            g_eventBus.handleEvent(events.LoadViewEvent(RANKEDBATTLES_ALIASES.RANKED_BATTLES_SEASON_COMPLETE, ctx={'quest': quest,
             'awards': data,
             'closeClb': self.__unlock}), scope=EVENT_BUS_SCOPE.LOBBY)
        else:
            self.__unlock()
        return

    def __showBoobyAwardWindow(self, quest):
        quests_events.showRankedBoobyAward(quest)
        self.__unlock()


class _NYBoxesHandler(AwardHandler):
    _newYearController = dependency.descriptor(INewYearController)

    def __init__(self, awardCtrl):
        super(_NYBoxesHandler, self).__init__(awardCtrl)
        self.__postponedBoxes = defaultdict(int)

    def init(self):
        self._newYearController.boxStorage.onCountChanged += self.__onBoxesCountChanged

    def fini(self):
        self._newYearController.boxStorage.onCountChanged -= self.__onBoxesCountChanged

    def __onBoxesCountChanged(self, _, __, addedInfo):
        if addedInfo:
            descrs = self._newYearController.boxStorage.getDescriptors()
            for bId, new_count in addedInfo.iteritems():
                self.__postponedBoxes[descrs[bId].setting] += new_count

            self.handle()

    def _showAward(self, ctx):
        for setting, new_count in self.__postponedBoxes.iteritems():
            g_eventBus.handleEvent(events.LoadViewEvent(VIEW_ALIAS.LOBBY_NY_MISSIONS_REWARD, name=getViewName(VIEW_ALIAS.LOBBY_NY_MISSIONS_REWARD, setting), ctx={'rewards': new_count,
             'setting': setting}), EVENT_BUS_SCOPE.LOBBY)

        self.__postponedBoxes = defaultdict(int)

    def _needToShowAward(self, ctx):
        return self.__isNY()

    @staticmethod
    def __isNY():
        player = BigWorld.player()
        if not hasattr(player, 'newYear'):
            return False
        return player.newYear.state == NY_STATE.IN_PROGRESS