# Embedded file name: scripts/client/gui/clans/clan_helpers.py
from datetime import datetime
from adisp import async, process
import Event
from gui.shared.utils import sortByFields
from collections import namedtuple
from debug_utils import LOG_DEBUG, LOG_WARNING
from gui.clans import interfaces, items
from gui.clans.contexts import SearchClansCtx, GetRecommendedClansCtx, AccountInvitesCtx, ClanRatingsCtx, ClansInfoCtx
from gui.clans.items import ClanInviteWrapper, ClanPersonalInviteWrapper
from gui.clans.settings import COUNT_THRESHOLD, CLAN_INVITE_STATES, DATA_UNAVAILABLE_PLACEHOLDER
from gui.shared.utils.ListPaginator import ListPaginator
from gui.shared.utils import getPlayerDatabaseID
from gui.shared.view_helpers import UsersInfoHelper
_RequestData = namedtuple('_RequestData', ['pattern',
 'offset',
 'count',
 'isReset',
 'isRecommended'])

class ClanListener(interfaces.IClanListener):

    @property
    def clansCtrl(self):
        from gui.clans.clan_controller import g_clanCtrl
        return g_clanCtrl

    def startClanListening(self):
        self.clansCtrl.addListener(self)

    def stopClanListening(self):
        self.clansCtrl.removeListener(self)


class ClanFinder(ListPaginator, UsersInfoHelper):

    def __init__(self, requester, offset = 0, count = 18):
        super(ClanFinder, self).__init__(requester, offset, count)
        self.__pattern = str()
        self.__lastResult = []
        self.__listMapping = {}
        self.__lastStatus = True
        self.__totalCount = None
        self.__isRecommended = False
        self.__lastSuccessRequestData = None
        self.__isSynced = False
        return

    def isSynced(self):
        return self.__isSynced

    def setPattern(self, pattern):
        self.__pattern = pattern

    def getPattern(self):
        return self.__pattern

    def getTotalCount(self):
        return self.__totalCount

    def getLastStatus(self):
        return self.__lastStatus

    def getLastResult(self):
        return self.__lastResult

    def isRecommended(self):
        return self.__isRecommended

    def setRecommended(self, isRecommended):
        self.__isRecommended = isRecommended

    def getItemByID(self, clanDbID):
        if clanDbID in self.__listMapping:
            return self.__lastResult[self.__listMapping[clanDbID]]
        else:
            return None

    def canMoveLeft(self):
        return self.__lastStatus and self._offset > 0

    def canMoveRight(self):
        return self.__lastStatus and self.__totalCount > self._offset + self._count

    def hasSuccessRequest(self):
        return self.__lastSuccessRequestData is not None

    def requestLastSuccess(self):
        if self.hasSuccessRequest():
            self.__isRecommended = self.__lastSuccessRequestData.isRecommended
            self.__pattern = self.__lastSuccessRequestData.pattern
            self._count = self.__lastSuccessRequestData.count
            self._offset = self.__lastSuccessRequestData.offset
            self._request(self.__lastSuccessRequestData.isReset)
        else:
            LOG_DEBUG('Has not been success result yet. Operation is unavailable.')

    @process
    def _request(self, isReset = False):
        self._offset = max(self._offset, 0)
        if self._offset > 0 and self._offset >= self.__totalCount:
            self._offset = self._offset - self._count
        if self.__isRecommended:
            ctx = GetRecommendedClansCtx(self._offset, self._count, True)
        else:
            ctx = SearchClansCtx(self.__pattern, self._offset, self._count, True)
        result = yield self._requester.sendRequest(ctx, allowDelay=True)
        self.__lastResult = ctx.getDataObj(result.data)
        self.__lastStatus = result.isSuccess()
        self.__totalCount = ctx.getTotalCount(result.data)
        self._invalidateMapping()
        for item in self.__lastResult:
            self.getUserName(item.getLeaderDbID())

        if result.isSuccess():
            self.__isSynced = True
            if not result.data:
                if not isReset:
                    self.revertOffset()
            elif self.isRecommended():
                self.__lastSuccessRequestData = _RequestData(self.__pattern, self._offset, self._count, isReset, self.__isRecommended)
        else:
            self.revertOffset()
        self.syncUsersInfo()
        self.onListUpdated(self._selectedID, True, True, (self.__lastStatus, self.__lastResult))

    def _invalidateMapping(self):
        self.__listMapping = {}
        if self.__lastResult is not None:
            for index, item in enumerate(self.__lastResult):
                self.__listMapping[item.getClanDbID()] = index

        return


class ClanInvitesPaginator(ListPaginator, UsersInfoHelper):

    def __init__(self, requester, contextClass, clanDbID, statuses = list(), offset = 0, count = 50):
        super(ClanInvitesPaginator, self).__init__(requester, offset, count)
        self.__ctxClass = contextClass
        self.__clanDbID = clanDbID
        self.__statuses = statuses
        self.__invitesCache = []
        self.__cacheMapping = {}
        self.__accountNameMapping = {}
        self.__senderNameMapping = {}
        self.__lastStatus = True
        self.__lastResult = []
        self.__totalCount = None
        self.__allInvitesCached = False
        self.__lastSort = tuple()
        self.__isInProgress = False
        self.__isSynced = False
        self.onListItemsUpdated = Event.Event(self._eManager)
        return

    def setStatuses(self, statuses):
        self.__statuses = statuses

    def getStatuses(self):
        return self.__statuses

    def getTotalCount(self):
        return self.__totalCount

    def canMoveLeft(self):
        return self.__lastStatus and self._offset > 0

    def canMoveRight(self):
        return self.__lastStatus and self.__totalCount > self._offset + self._count

    def isInProgress(self):
        return self.__isInProgress

    def isSynced(self):
        return self.__isSynced

    def markAsUnSynced(self):
        self.__isSynced = False

    def getLastStatus(self):
        return self.__lastStatus

    def getLastResult(self):
        return self.__lastResult

    def getLastSort(self):
        return self.__lastSort

    def sort(self, sort):
        self._selectedID = None
        self._offset = self.getInitialOffset()
        self._prevOffset = self._offset
        self._request(isReset=True, sort=sort)
        return

    def refresh(self):
        sort = self.__lastSort
        self.__invitesCache = []
        self.__lastStatus = False
        self.__allInvitesCached = False
        self.__lastSort = tuple()
        self._selectedID = None
        self._offset = self.getInitialOffset()
        self._prevOffset = self._offset
        self._request(isReset=True, sort=sort)
        return

    def accept(self, inviteDbId, context):
        invite = self.getInviteByDbID(inviteDbId)
        if invite is not None:
            self.__sendRequest(invite, context, CLAN_INVITE_STATES.ACCEPTED)
        return

    def decline(self, inviteDbId, context):
        invite = self.getInviteByDbID(inviteDbId)
        if invite is not None:
            self.__sendRequest(invite, context, CLAN_INVITE_STATES.DECLINED)
        return

    def resend(self, inviteDbId, context):
        invite = self.getInviteByDbID(inviteDbId)
        if invite is not None:
            if invite.getStatus() == CLAN_INVITE_STATES.EXPIRED:
                self.__sendRequest(invite, context, CLAN_INVITE_STATES.EXPIRED_RESENT)
            elif invite.getStatus() == CLAN_INVITE_STATES.DECLINED:
                self.__sendRequest(invite, context, CLAN_INVITE_STATES.DECLINED_RESENT)
        return

    def getInviteByDbID(self, inviteDbID):
        index = self.__cacheMapping.get(inviteDbID, -1)
        if index >= 0:
            return self.__invitesCache[index]
        else:
            return None

    def onUserNamesReceived(self, names):
        updatedInvites = set()
        for userID, name in names.iteritems():
            for inviteID in self.__accountNameMapping.get(userID, tuple()):
                invite = self.getInviteByDbID(inviteID)
                if invite is not None:
                    invite.setUserName(name)
                    updatedInvites.add(inviteID)

            for inviteID in self.__senderNameMapping.get(userID, tuple()):
                invite = self.getInviteByDbID(inviteID)
                if invite is not None:
                    invite.setSenderName(name)
                    updatedInvites.add(inviteID)

        if len(updatedInvites):
            self.onListItemsUpdated(self, [ self.__invitesCache[self.__cacheMapping[invID]] for invID in updatedInvites ])
        return

    @process
    def _request(self, isReset = False, sort = tuple()):
        self.__isInProgress = True
        self._offset = max(self._offset, 0)
        offset = 0
        count = self._offset + self._count
        if not self.__allInvitesCached:
            if len(sort):
                yield self.__requestInvites(0, COUNT_THRESHOLD, isReset)
                self.__allInvitesCached = self.__lastStatus
            else:
                yield self.__requestInvites(offset, count, isReset)
        self.__lastResult = []
        if self.__lastStatus:
            if sort is not None and sort != self.__lastSort:
                self.__invitesCache = sortByFields(sort, self.__invitesCache, valueGetter=getattr)
                self.__lastSort = sort
                self.__rebuildMapping()
            self.__lastResult = self.__getSlice(offset, count)
        self.__isInProgress = False
        self.onListUpdated(self._selectedID, True, True, (self.__lastStatus, self.__lastResult))
        return

    def __getSlice(self, offset, count):
        result = list()
        total = len(self.__invitesCache)
        if total > offset + count:
            result = self.__invitesCache[offset:count]
        elif total > offset:
            result = self.__invitesCache[offset:]
        return result

    @async
    @process
    def __requestInvites(self, offset, count, isReset, callback):
        ctx = self.__ctxClass(clanDbID=self.__clanDbID, offset=offset, limit=count, statuses=self.__statuses, getTotalCount=isReset)
        result = yield self._requester.sendRequest(ctx, allowDelay=True)
        invites = ctx.getDataObj(result.data)
        self.__lastStatus = result.isSuccess()
        if isReset:
            self.__totalCount = ctx.getTotalCount(result.data)
        if result.isSuccess():
            if len(invites) == 0 and not isReset:
                self.revertOffset()
            usrIDs = set()
            for item in invites:
                usrIDs.add(item.getAccountDbID())
                temp = self.__accountNameMapping.get(item.getAccountDbID(), set())
                temp.add(item.getDbID())
                self.__accountNameMapping[item.getAccountDbID()] = temp
                usrIDs.add(item.getSenderDbID())
                temp = self.__senderNameMapping.get(item.getSenderDbID(), set())
                temp.add(item.getDbID())
                self.__senderNameMapping[item.getSenderDbID()] = temp

            self.__lastStatus, users = yield self._requester.requestUsers(usrIDs)
            if self.__lastStatus:
                self.__invitesCache = [ ClanInviteWrapper(invite, users.get(invite.getAccountDbID(), items.AccountClanRatingsData(invite.getAccountDbID())), self.getUserName(invite.getAccountDbID()), users.get(invite.getSenderDbID(), items.AccountClanRatingsData(invite.getSenderDbID())), self.getUserName(invite.getSenderDbID())) for invite in invites ]
            else:
                self.__invitesCache = []
                self.revertOffset()
        else:
            self.__invitesCache = []
            self.revertOffset()
        self.__rebuildMapping()
        self.syncUsersInfo()
        self.__isSynced = True
        callback((self.__lastStatus, self.__invitesCache))

    def __rebuildMapping(self):
        self.__cacheMapping = dict(((invite.getDbID(), index) for index, invite in enumerate(self.__invitesCache)))

    @process
    def __sendRequest(self, invite, context, sucessStatus):
        self.__isInProgress = True
        userDbID = getPlayerDatabaseID()
        temp = self.__accountNameMapping.get(userDbID, set())
        temp.add(invite.getDbID())
        self.__accountNameMapping[userDbID] = temp
        result = yield self._requester.sendRequest(context, allowDelay=True)
        if result.isSuccess():
            status = sucessStatus
        else:
            status = CLAN_INVITE_STATES.ERROR
        result, users = yield self._requester.requestUsers([userDbID])
        sender = users.get(userDbID, items.AccountClanRatingsData(userDbID))
        senderName = self.getUserName(userDbID)
        item = self.__updateInvite(invite, status, sender, senderName)
        self.syncUsersInfo()
        self.__isInProgress = False
        self.onListItemsUpdated(self, [item])

    def __updateInvite(self, inviteWrapper, status, sender, senderName):
        invite = inviteWrapper.invite.update(status=status, sender_id=sender.getAccountDbID(), created_at=datetime.now(), updated_at=datetime.now())
        inviteWrapper.setInvite(invite)
        inviteWrapper.setSender(sender)
        inviteWrapper.setSenderName(senderName)
        return inviteWrapper

    def __checkUserName(self, name):
        if not len(name):
            return DATA_UNAVAILABLE_PLACEHOLDER
        return name


class ClanPersonalInvitesPaginator(ListPaginator, UsersInfoHelper):

    def __init__(self, requester, accountDbID, statuses = list(), offset = 0, count = 50):
        super(ClanPersonalInvitesPaginator, self).__init__(requester, offset, count)
        self.__accountDbID = accountDbID
        self.__statuses = statuses
        self.__invitesCache = []
        self.__cacheMapping = {}
        self.__lastStatus = True
        self.__lastResult = []
        self.__totalCount = None
        self.__allInvitesCached = False
        self.__lastSort = tuple()
        self.__isInProgress = False
        self.__isSynced = False
        self.__sentRequestCount = 0
        self.__senderNameMapping = {}
        self.onListItemsUpdated = Event.Event(self._eManager)
        return

    def setStatuses(self, statuses):
        self.__statuses = statuses

    def getStatuses(self):
        return self.__statuses

    def getTotalCount(self):
        return self.__totalCount

    def canMoveLeft(self):
        return self.__lastStatus and self._offset > 0

    def canMoveRight(self):
        return self.__lastStatus and self.__totalCount > self._offset + self._count

    def isInProgress(self):
        return self.__isInProgress

    def isSynced(self):
        return self.__isSynced

    def markAsUnSynced(self):
        self.__isSynced = False

    def getLastStatus(self):
        return self.__lastStatus

    def getLastResult(self):
        return self.__lastResult

    def getLastSort(self):
        return self.__lastSort

    def sort(self, sort):
        self._selectedID = None
        self._offset = self.getInitialOffset()
        self._prevOffset = self._offset
        self._request(isReset=True, sort=sort)
        return

    def refresh(self):
        sort = self.__lastSort
        self.__invitesCache = []
        self.__lastStatus = False
        self.__allInvitesCached = False
        self.__lastSort = tuple()
        self._selectedID = None
        self._offset = self.getInitialOffset()
        self._prevOffset = self._offset
        self._request(isReset=True, sort=sort)
        return

    def accept(self, contexts):
        for context in contexts:
            self.__sendADRequest(context, CLAN_INVITE_STATES.ACCEPTED)

    def decline(self, contexts):
        for context in contexts:
            self.__sendADRequest(context, CLAN_INVITE_STATES.DECLINED)

    def getInviteByDbID(self, inviteDbID):
        index = self.__cacheMapping.get(inviteDbID, -1)
        if index >= 0:
            return self.__invitesCache[index]
        else:
            return None

    def onUserNamesReceived(self, names):
        updatedInvites = set()
        for userID, name in names.iteritems():
            for inviteID in self.__senderNameMapping.get(userID, tuple()):
                invite = self.getInviteByDbID(inviteID)
                if invite is not None:
                    invite.setSenderName(name)
                    updatedInvites.add(inviteID)

        if len(updatedInvites):
            self.onListItemsUpdated(self, [ self.__invitesCache[self.__cacheMapping[invID]] for invID in updatedInvites ])
        return

    @process
    def _request(self, isReset = False, sort = tuple()):
        self.__sentRequestCount += 1
        self._offset = max(self._offset, 0)
        offset = 0
        count = self._offset + self._count
        if not self.__allInvitesCached:
            if len(sort):
                yield self.__requestInvites(0, COUNT_THRESHOLD, isReset)
                self.__allInvitesCached = self.__lastStatus
            else:
                yield self.__requestInvites(offset, count, isReset)
        self.__lastResult = []
        if self.__lastStatus:
            if sort is not None and sort != self.__lastSort:
                self.__invitesCache = sortByFields(sort, self.__invitesCache, valueGetter=getattr)
                self.__lastSort = sort
                self.__rebuildMapping()
            self.__lastResult = self.__getSlice(offset, count)
        self.__sentRequestCount -= 1
        self.__isInProgress = self.__sentRequestCount > 0
        self.onListUpdated(self._selectedID, True, True, (self.__lastStatus, self.__lastResult))
        return

    def __getSlice(self, offset, count):
        result = list()
        total = len(self.__invitesCache)
        if total > offset + count:
            result = self.__invitesCache[offset:count]
        elif total > offset:
            result = self.__invitesCache[offset:]
        return result

    @async
    @process
    def __requestInvites(self, offset, count, isReset, callback):
        ctx = AccountInvitesCtx(accountDbID=self.__accountDbID, offset=offset, limit=count, statuses=self.__statuses, getTotalCount=isReset)
        result = yield self._requester.sendRequest(ctx, allowDelay=True)
        invites = ctx.getDataObj(result.data)
        self.__lastStatus = result.isSuccess()
        if isReset:
            self.__totalCount = ctx.getTotalCount(result.data)
        if result.isSuccess():
            if len(invites) == 0 and not isReset:
                self.revertOffset()
            if len(invites) > 0:
                clansIDs = [ item.getClanDbID() for item in invites ]
                ctx = ClanRatingsCtx(clansIDs)
                result = yield self._requester.sendRequest(ctx, allowDelay=True)
                clanRatings = dict(((item.getClanDbID(), item) for item in ctx.getDataObj(result.data)))
                ctx = ClansInfoCtx(clansIDs)
                result = yield self._requester.sendRequest(ctx, allowDelay=True)
                clanInfo = dict(((item.getDbID(), item) for item in ctx.getDataObj(result.data)))
                for item in clanInfo.itervalues():
                    self.getUserName(item.getLeaderDbID())

                for item in invites:
                    temp = self.__senderNameMapping.get(item.getSenderDbID(), set())
                    temp.add(item.getDbID())
                    self.__senderNameMapping[item.getSenderDbID()] = temp

                self.__invitesCache = [ ClanPersonalInviteWrapper(invite, clanInfo.get(invite.getClanDbID(), items.ClanExtInfoData()), clanRatings.get(invite.getClanDbID(), items.ClanRatingsData()), self.getUserName(invite.getSenderDbID())) for invite in invites ]
            else:
                self.__invitesCache = []
        else:
            self.__invitesCache = []
            self.revertOffset()
        self.__rebuildMapping()
        self.syncUsersInfo()
        self.__isSynced = True
        callback((self.__lastStatus, self.__invitesCache))

    def __rebuildMapping(self):
        self.__cacheMapping = dict(((invite.getDbID(), index) for index, invite in enumerate(self.__invitesCache)))

    @process
    def __sendADRequest(self, context, sucessStatus):
        self.__isInProgress = True
        self.__sentRequestCount += 1
        result = yield self._requester.sendRequest(context, allowDelay=True)
        inviteDbID = context.getInviteDbID()
        if result.isSuccess():
            status = sucessStatus
        else:
            status = CLAN_INVITE_STATES.ERROR
        self.__sentRequestCount -= 1
        self.__isInProgress = self.__sentRequestCount > 0
        inviteWrapper = self.getInviteByDbID(inviteDbID)
        if inviteWrapper:
            invite = inviteWrapper.invite.update(status=status)
            inviteWrapper.setInvite(invite)
            self.onListItemsUpdated(self, [inviteWrapper])
        else:
            LOG_WARNING('Could not find invite with DB ID {} in the internal cache. Received data - "{}"'.format(inviteDbID, result.data))