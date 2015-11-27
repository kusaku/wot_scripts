# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/clans/profile/ClanProfilePersonnelView.py
from collections import defaultdict
import BigWorld
from adisp import process
from constants import CLAN_MEMBER_FLAGS
from debug_utils import LOG_ERROR, LOG_WARNING
from gui.shared.utils import sortByFields
from helpers import i18n
from account_helpers import getAccountDatabaseID
from gui.Scaleform.daapi.view.lobby.clans.profile import MAX_MEMBERS_IN_CLAN
from gui.Scaleform.daapi.view.lobby.profile.ProfileUtils import HeaderItemsTypes, ProfileUtils
from gui.Scaleform.daapi.view.meta.ClanProfilePersonnelViewMeta import ClanProfilePersonnelViewMeta
from gui.Scaleform.framework.entities.DAAPIDataProvider import SortableDAAPIDataProvider
from gui.Scaleform.locale.CLANS import CLANS
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.shared.formatters import text_styles
from gui.shared.event_dispatcher import showClanInvitesWindow
from gui.shared.view_helpers import UsersInfoHelper
from gui.clans.settings import CLIENT_CLAN_RESTRICTIONS as RES, DATA_UNAVAILABLE_PLACEHOLDER
from gui.clans import formatters as clans_fmts
from helpers.i18n import makeString as _ms
from helpers.time_utils import getTimeDeltaTilNow, ONE_DAY
from messenger.gui.Scaleform.data.contacts_vo_converter import ContactConverter
from messenger.proto.bw.find_criteria import BWClanChannelFindCriteria
from messenger.proto.events import g_messengerEvents
from messenger.storage import storage_getter
OPEN_INVITES_ACTION_ID = 'openInvites'
OPEN_CLAN_CHANNEL_ACTION_ID = 'openClanChannel'
_CLAN_MEMBERS_SORT_INDEXES = (CLAN_MEMBER_FLAGS.LEADER,
 CLAN_MEMBER_FLAGS.VICE_LEADER,
 CLAN_MEMBER_FLAGS.STAFF,
 CLAN_MEMBER_FLAGS.COMMANDER,
 CLAN_MEMBER_FLAGS.DIPLOMAT,
 CLAN_MEMBER_FLAGS.TREASURER,
 CLAN_MEMBER_FLAGS.RECRUITER,
 CLAN_MEMBER_FLAGS.JUNIOR,
 CLAN_MEMBER_FLAGS.PRIVATE,
 CLAN_MEMBER_FLAGS.RECRUIT,
 CLAN_MEMBER_FLAGS.RESERVIST)

class _SORT_IDS:
    USER_NAME = 'userName'
    POST = 'post'
    RATING = 'rating'
    BATTLES_COUNT = 'battlesCount'
    BATTLES_PERFORMANCE = 'battlesPerformance'
    AWG_XP = 'awgXP'
    DAYS_IN_CLAN = 'daysInClan'


def _packStat(text, description, tooltip, icon):
    return {'type': HeaderItemsTypes.COMMON,
     'text': text,
     'description': _ms(description),
     'iconPath': ProfileUtils.getIconPath(icon),
     'tooltip': tooltip,
     'enabled': True}


def _packColumn(columdID, label, buttonWidth, tooltip, icon = '', sortOrder = -1, showSeparator = True):
    return {'id': columdID,
     'label': _ms(label),
     'iconSource': icon,
     'buttonWidth': buttonWidth,
     'toolTip': tooltip,
     'sortOrder': sortOrder,
     'defaultSortDirection': 'ascending',
     'buttonHeight': 34,
     'showSeparator': showSeparator}


class ClanProfilePersonnelView(ClanProfilePersonnelViewMeta):

    def __init__(self):
        super(ClanProfilePersonnelView, self).__init__()
        self.__membersDP = None
        return

    @storage_getter('channels')
    def channelsStorage(self):
        return None

    @process
    def setClanDossier(self, clanDossier):
        super(ClanProfilePersonnelView, self).setClanDossier(clanDossier)
        self._showWaiting()
        self.__membersDP = _ClanMembersDataProvider()
        self.__membersDP.setFlashObject(self.as_getMembersDPS())
        clanInfo = yield clanDossier.requestClanInfo()
        members = yield clanDossier.requestMembers()
        if self.isDisposed():
            return
        self._updateClanInfo(clanInfo)
        membersCount = len(members)
        self.__membersDP.buildList(members, syncUserInfo=True)
        totalRatings = self.__membersDP.getTotalRatings()
        statistics = [_packStat(BigWorld.wg_getIntegralFormat(totalRatings.getAvgGlobalRating()), CLANS.PERSONNELVIEW_CLANSTATS_AVGPERSONALRATING, CLANS.PERSONNELVIEW_CLANSTATS_AVGPERSONALRATING_TOOLTIP, 'avgPersonalRating40x32.png'),
         _packStat(BigWorld.wg_getIntegralFormat(totalRatings.getAvgBattlesCount()), CLANS.PERSONNELVIEW_CLANSTATS_AVGBATTLESCOUNT, CLANS.PERSONNELVIEW_CLANSTATS_AVGBATTLESCOUNT_TOOLTIP, 'avgBattlesCount40x32.png'),
         _packStat(BigWorld.wg_getNiceNumberFormat(totalRatings.getAvgPerformanceBattles()) + '%', CLANS.PERSONNELVIEW_CLANSTATS_AVGWINS, CLANS.PERSONNELVIEW_CLANSTATS_AVGWINS_TOOLTIP, 'avgWins40x32.png'),
         _packStat(BigWorld.wg_getIntegralFormat(totalRatings.getAvgXp()), CLANS.PERSONNELVIEW_CLANSTATS_AVGEXP, CLANS.PERSONNELVIEW_CLANSTATS_AVGEXP_TOOLTIP, 'avgExp40x32.png')]
        headers = [_packColumn(_SORT_IDS.USER_NAME, CLANS.PERSONNELVIEW_TABLE_PLAYER, 223, CLANS.PERSONNELVIEW_TABLE_PLAYER_TOOLTIP),
         _packColumn(_SORT_IDS.POST, CLANS.PERSONNELVIEW_TABLE_POST, 275, CLANS.PERSONNELVIEW_TABLE_POST_TOOLTIP),
         _packColumn(_SORT_IDS.RATING, '', 100, CLANS.PERSONNELVIEW_TABLE_PERSONALRATING_TOOLTIP, RES_ICONS.MAPS_ICONS_STATISTIC_RATING24),
         _packColumn(_SORT_IDS.BATTLES_COUNT, '', 100, CLANS.PERSONNELVIEW_TABLE_BATTLESCOUNT_TOOLTIP, RES_ICONS.MAPS_ICONS_STATISTIC_BATTLES24),
         _packColumn(_SORT_IDS.BATTLES_PERFORMANCE, '', 100, CLANS.PERSONNELVIEW_TABLE_WINS_TOOLTIP, RES_ICONS.MAPS_ICONS_STATISTIC_WINS24),
         _packColumn(_SORT_IDS.AWG_XP, '', 100, CLANS.PERSONNELVIEW_TABLE_AVGEXP_TOOLTIP, RES_ICONS.MAPS_ICONS_STATISTIC_AVGEXP24),
         _packColumn(_SORT_IDS.DAYS_IN_CLAN, '', 100, CLANS.PERSONNELVIEW_TABLE_DAYSINCLAN_TOOLTIP, RES_ICONS.MAPS_ICONS_STATISTIC_DAYSINCLAN24, showSeparator=False)]
        self.as_setDataS({'membersCount': _ms(CLANS.PERSONNELVIEW_MEMBERSCOUNT, count=text_styles.stats(str(membersCount)), max=str(MAX_MEMBERS_IN_CLAN)),
         'tableHeaders': headers,
         'statistics': statistics,
         'defaultSortField': _SORT_IDS.POST,
         'defaultSortDirection': 'ascending'})
        self._updateHeaderState()
        self._hideWaiting()

    def onHeaderButtonClick(self, actionID):
        if actionID == OPEN_CLAN_CHANNEL_ACTION_ID:
            channel = self.channelsStorage.getChannelByCriteria(BWClanChannelFindCriteria())
            if channel is not None:
                g_messengerEvents.channels.onPlayerEnterChannelByAction(channel)
            else:
                LOG_WARNING("Clan channel couldn't find!")
        elif actionID == OPEN_INVITES_ACTION_ID:
            showClanInvitesWindow()
        else:
            super(ClanProfilePersonnelView, self).onHeaderButtonClick(actionID)
        return

    def onAccountClanProfileChanged(self, profile):
        self._updateHeaderState()

    def onClanAppsCountReceived(self, clanDbID, appsCount):
        if self._clanDossier.getDbID() == clanDbID:
            self._updateHeaderState()

    def _updateHeaderState(self):
        limits = self.clansCtrl.getLimits()
        if limits.canAcceptApplication(self._clanDossier).success or limits.canDeclineApplication(self._clanDossier).success:
            vo = self._getHeaderButtonStateVO(False, None, True, True, False, OPEN_INVITES_ACTION_ID)
            if self._clanDossier.isSynced('appsCount'):
                vo['iconBtnLabel'] = '  ' + clans_fmts.formatDataToString(self._clanDossier.getAppsCount())
            else:
                vo['iconBtnLabel'] = DATA_UNAVAILABLE_PLACEHOLDER
            vo['iconBtnIcon'] = 'envelope.png'
            self.as_setHeaderStateS(vo)
        else:
            super(ClanProfilePersonnelView, self)._updateHeaderState()
        return

    def _initHeaderBtnStates(self):
        states = super(ClanProfilePersonnelView, self)._initHeaderBtnStates()
        states[RES.OWN_CLAN] = self._getHeaderButtonStateVO(True, i18n.makeString(CLANS.CLAN_HEADER_CHATCHANNELBTN), actionId=OPEN_CLAN_CHANNEL_ACTION_ID, actionBtnTooltip=CLANS.CLAN_HEADER_CHATCHANNELBTN_TOOLTIP)
        return states


class _MembersClanRating(object):

    def __init__(self):
        self.__total = defaultdict(int)
        self.__membersCount = 0

    def __iadd__(self, accRating):
        self.__membersCount += 1
        self.__total['globalRating'] += accRating.getGlobalRating()
        self.__total['battlesCount'] += accRating.getBattlesCount()
        self.__total['perfAvg'] += accRating.getBattlesPerformanceAvg()
        self.__total['xp'] += accRating.getXp()
        return self

    def clear(self):
        self.__membersCount = 0
        self.__total.clear()

    def getAvgGlobalRating(self):
        return self.__getAvgValue('globalRating')

    def getAvgBattlesCount(self):
        return self.__getAvgValue('battlesCount')

    def getAvgPerformanceBattles(self):
        return self.__getAvgValue('perfAvg')

    def getAvgXp(self):
        return self.__getAvgValue('xp')

    def __getAvgValue(self, key):
        if self.__membersCount:
            return self.__total[key] / self.__membersCount
        return 0


class _ClanMembersDataProvider(SortableDAAPIDataProvider, UsersInfoHelper):

    def __init__(self):
        super(_ClanMembersDataProvider, self).__init__()
        self._list = []
        self.__mapping = {}
        self.__selectedID = None
        self.__totalRatings = _MembersClanRating()
        self.__accountsList = []
        self.__sortMapping = {_SORT_IDS.USER_NAME: self.__getMemberName,
         _SORT_IDS.POST: self.__getMemberRole,
         _SORT_IDS.RATING: self.__getMemberRating,
         _SORT_IDS.BATTLES_COUNT: self.__getMemberBattlesCount,
         _SORT_IDS.BATTLES_PERFORMANCE: self.__getMemberBattlesPerformance,
         _SORT_IDS.AWG_XP: self.__getMemberAwgExp,
         _SORT_IDS.DAYS_IN_CLAN: self.__getMemberDaysInClan}
        return

    @storage_getter('users')
    def userStorage(self):
        return None

    @property
    def collection(self):
        return self._list

    @property
    def sortedCollection(self):
        return self._list

    def emptyItem(self):
        return None

    def clear(self):
        self._list = []
        self.__accountsList = []
        self.__mapping.clear()
        self.__selectedID = None
        return

    def fini(self):
        self.clear()
        self._dispose()

    def getTotalRatings(self):
        return self.__totalRatings

    def getSelectedIdx(self):
        if self.__selectedID in self.__mapping:
            return self.__mapping[self.__selectedID]
        return -1

    def setSelectedID(self, id):
        self.__selectedID = id

    def getVO(self, index):
        vo = None
        if index > -1:
            try:
                vo = self.sortedCollection[index]
            except IndexError:
                LOG_ERROR('Item not found', index)

        return vo

    def buildList(self, accounts, syncUserInfo = False):
        self.clear()
        self.__totalRatings.clear()
        self.__accountsList = accounts
        self._list = list((self._makeVO(acc) for acc in accounts))
        if syncUserInfo:
            self.syncUsersInfo()

    def refreshItem(self, cache, clanDBID):
        isSelected = self.__selectedID == clanDBID
        self.buildList(cache)
        if isSelected and clanDBID not in self.__mapping:
            return True
        return False

    def pyGetSelectedIdx(self):
        return self.getSelectedIdx()

    def onUserNamesReceived(self, names):
        if self.__accountsList and len(names):
            self.buildList(self.__accountsList)
            self.refresh()

    def pySortOn(self, fields, order):
        super(_ClanMembersDataProvider, self).pySortOn(fields, order)
        if self.__accountsList:
            self.__accountsList = sortByFields(self._sort, self.__accountsList, valueGetter=self.__sortingMethod)
            self.buildList(self.__accountsList)
            self.refresh()

    def _makeVO(self, memberData):
        memberDBID = memberData.getDbID()
        contactEntity = self.userStorage.getUser(memberDBID)
        if not contactEntity:
            return None
        else:
            userVO = ContactConverter().makeVO(contactEntity)
            ratings = memberData.getRatings()
            self.__totalRatings += ratings
            return {'dbID': memberDBID,
             'userName': self.__getMemberName(memberData),
             'post': memberData.getRoleString(),
             'postIcon': memberData.getRoleIcon(),
             'personalRating': BigWorld.wg_getIntegralFormat(self.__getMemberRating(memberData)),
             'battlesCount': BigWorld.wg_getIntegralFormat(self.__getMemberBattlesCount(memberData)),
             'wins': BigWorld.wg_getNiceNumberFormat(self.__getMemberBattlesPerformance(memberData)) + '%',
             'awgExp': BigWorld.wg_getIntegralFormat(self.__getMemberAwgExp(memberData)),
             'daysInClan': BigWorld.wg_getIntegralFormat(self.__getMemberDaysInClan(memberData)),
             'canShowContextMenu': memberDBID != getAccountDatabaseID(),
             'contactItem': userVO}

    def __sortingMethod(self, item, field):
        valueGetter = self.__sortMapping[field]
        return valueGetter(item)

    def __getMemberName(self, memberData):
        return self.getUserName(memberData.getDbID())

    def __getMemberRole(self, memberData):
        return _CLAN_MEMBERS_SORT_INDEXES.index(memberData.getRole())

    def __getMemberRating(self, memberData):
        return memberData.getRatings().getGlobalRating()

    def __getMemberBattlesCount(self, memberData):
        return memberData.getRatings().getBattlesCount()

    def __getMemberBattlesPerformance(self, memberData):
        return memberData.getRatings().getBattlesPerformanceAvg()

    def __getMemberAwgExp(self, memberData):
        return memberData.getRatings().getXp()

    def __getMemberDaysInClan(self, memberData):
        return getTimeDeltaTilNow(memberData.getJoiningTime()) / ONE_DAY