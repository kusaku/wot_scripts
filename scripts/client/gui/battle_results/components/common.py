# Embedded file name: scripts/client/gui/battle_results/components/common.py
import BigWorld
from constants import ARENA_GUI_TYPE, FINISH_REASON
from gui.Scaleform.locale.BATTLE_RESULTS import BATTLE_RESULTS
from gui.Scaleform.locale.RANKED_BATTLES import RANKED_BATTLES
from gui.Scaleform.genConsts.RANKEDBATTLES_ALIASES import RANKEDBATTLES_ALIASES
from gui.battle_results.components import base
from gui.battle_results.components import style
from gui.battle_results.settings import PLAYER_TEAM_RESULT as _TEAM_RESULT, UI_VISIBILITY
from gui.ranked_battles.ranked_models import RANK_CHANGE_STATES
from gui.shared.fortifications.FortBuilding import FortBuilding
from skeletons.gui.game_control import IRankedBattlesController
from helpers import i18n, dependency
_ARENA_TYPE_FORMAT = '#arenas:type/{0}/name'
_ARENA_TYPE_EXT_FORMAT = '#menu:loading/battleTypes/{0}'
_ARENA_FULL_NAME_FORMAT = '{0} - {1}'
_ARENA_ICON_PATH = '../maps/icons/map/stats/%s.png'
_FULL_RESULT_LABEL = '#menu:finalStatistic/commonStats/resultlabel/{0}'
_FINISH_REASON_LABEL = '#battle_results:finish/reason/{0}'
_FORT_BATTLE_SHORT_RESULT = 'clanBattle_{}'
_FORT_BATTLE_FINISH_REASON_DEF = '#battle_results:finish/clanBattle_reason_def/1{0}'
_FORT_BATTLE_FINISH_REASON_ATTACK = '#battle_results:finish/clanBattle_reason_attack/1{0}'
_FALLOUT_RESULT_LABEL = '#battle_results:fallout/{submode}/{status}'

def makeArenaFullName(arenaTypeName, i18nKey):
    """Returns i18n string containing full name of arena.
    :param arenaTypeName: string containing name of arena.
    :param i18nKey: string containing i18n key.
    :return: i18n string.
    """
    return _ARENA_FULL_NAME_FORMAT.format(i18n.makeString(arenaTypeName), i18n.makeString(i18nKey))


def makeRegularFinishResultLabel(finishReason, teamResult):
    """Returns i18n string describing finish reason of regular battle.
    :param finishReason: integer containing one of FINISH_REASON.*.
    :param teamResult: string containing one of PLAYER_TEAM_RESULT.*.
    :return: i18n string.
    """
    if finishReason == FINISH_REASON.EXTERMINATION:
        return i18n.makeString(_FINISH_REASON_LABEL.format(''.join((str(finishReason), str(teamResult)))))
    else:
        return i18n.makeString(_FINISH_REASON_LABEL.format(finishReason))


def makeFortBattleFinishResultLabel(teamResult, isDefender, buildingName):
    """Returns i18n string describing finish reason of fort battle..
    :param teamResult: string containing one of PLAYER_TEAM_RESULT.*.
    :param isDefender: did player's team defend building?
    :param buildingName: i18n string containing name of building
    :return: i18n string.
    """
    if isDefender:
        return i18n.makeString(_FORT_BATTLE_FINISH_REASON_DEF.format(teamResult), buildingName=buildingName)
    else:
        return i18n.makeString(_FORT_BATTLE_FINISH_REASON_ATTACK.format(teamResult), buildingName=buildingName)


class RankInfoHelper(object):
    """
    Helper class for filling RankChangesBlock.
    """
    rankedController = dependency.descriptor(IRankedBattlesController)
    __TITLE_LABEL_MAP = {RANK_CHANGE_STATES.RANK_EARNED: RANKED_BATTLES.BATTLERESULT_RANKEARNED,
     RANK_CHANGE_STATES.RANK_LOST: RANKED_BATTLES.BATTLERESULT_RANKLOST,
     RANK_CHANGE_STATES.STEP_EARNED: RANKED_BATTLES.BATTLERESULT_STAGEEARNED,
     RANK_CHANGE_STATES.STEP_LOST: RANKED_BATTLES.BATTLERESULT_STAGELOST,
     RANK_CHANGE_STATES.NOTHING_CHANGED: RANKED_BATTLES.BATTLERESULT_STAGENOTEARNED}
    __DESCRIPTION_LABEL_MAP = {RANK_CHANGE_STATES.RANK_EARNED: RANKED_BATTLES.getBattleResultsInTop,
     RANK_CHANGE_STATES.RANK_LOST: RANKED_BATTLES.getBattleResultsNotInTop,
     RANK_CHANGE_STATES.STEP_EARNED: RANKED_BATTLES.getBattleResultsInTop,
     RANK_CHANGE_STATES.STEP_LOST: RANKED_BATTLES.getBattleResultsNotInTop,
     RANK_CHANGE_STATES.NOTHING_CHANGED: RANKED_BATTLES.getBattleResultsNotInTop}
    __STATE_LABEL_MAP = {RANK_CHANGE_STATES.RANK_EARNED: (True, True, RANKEDBATTLES_ALIASES.getStateRankEarned),
     RANK_CHANGE_STATES.RANK_LOST: (True, False, RANKEDBATTLES_ALIASES.getStateRankLost),
     RANK_CHANGE_STATES.STEP_EARNED: (False, True, RANKEDBATTLES_ALIASES.getStateStageEarned),
     RANK_CHANGE_STATES.STEP_LOST: (False, False, RANKEDBATTLES_ALIASES.STATE_STAGE_LOST),
     RANK_CHANGE_STATES.NOTHING_CHANGED: (False, True, RANKEDBATTLES_ALIASES.getStateStageNotEarned)}

    def __init__(self, reusable):
        self.__reusable = reusable

    def getState(self):
        """
        Return a state, describing changes: is it rank or step changes.
        :return: one from self.STATES
        """
        return self.rankedController.getRankChangeStatus(self.__reusable.personal.getRankInfo())

    def makeStateLabel(self):
        """
        Returns 'state' field for RankChangesBlock
        :return: string, one from RANKEDBATTLES_ALIASES constants
        """
        rankInfo = self.__reusable.personal.getRankInfo()
        rankAfterBattle = rankInfo.accRank
        if rankAfterBattle == self.rankedController.getAccRanksTotal() and rankInfo.vehRank > 0:
            rankAfterBattle += 1
        if self.getState() == RANK_CHANGE_STATES.RANK_LOST:
            rankAfterBattle += 1
        isRankArgNecessary, isTopNumberArgNecessary, state = self.__STATE_LABEL_MAP[self.getState()]
        if isRankArgNecessary and isTopNumberArgNecessary:
            result = state(rankAfterBattle, self.__getTopBoundForPersonalTeam())
        elif isRankArgNecessary and not isTopNumberArgNecessary:
            result = state(rankAfterBattle)
        elif isTopNumberArgNecessary:
            result = state(self.__getTopBoundForPersonalTeam())
        else:
            result = state
        return result

    def makeTitleLabel(self):
        """
        Returns 'title' field for RankChangesBlock
        :return: string, one from RANKED_BATTLES constants
        """
        return self.__TITLE_LABEL_MAP[self.getState()]

    def makeDescriptionLabel(self):
        """
        Returns 'description' field for RankChangesBlock
        :return: string, one from RANKED_BATTLES constants
        """
        descriptionMethod = self.__DESCRIPTION_LABEL_MAP[self.getState()]
        return descriptionMethod(self.__getTopBoundForPersonalTeam())

    def getTopBoundForTeam(self, team):
        """
        Returns a top bound for the team(integer value) depending on battle result.
        For example: Win - TOP_12, Lose - TOP_3
        :param team: team index
        """
        if self.__reusable.common.winnerTeam == team:
            return self.getWinnerTopBound()
        return self.getLoserTopBound()

    @staticmethod
    def getWinnerTopBound():
        return 12

    @staticmethod
    def getLoserTopBound():
        return 3

    def __getTopBoundForPersonalTeam(self):
        """
        Returns a top bound for self team(integer value) depending on battle result.
        """
        return self.getTopBoundForTeam(self.__reusable.getPersonalTeam())


class ArenaShortTimeVO(base.StatsItem):
    __slots__ = ()

    def _convert(self, record, reusable):
        return style.makeTimeStatsVO(self._field, BigWorld.wg_getShortTimeFormat(record))


class ArenaDateTimeItem(base.StatsItem):
    __slots__ = ()

    def _convert(self, record, reusable):
        return ' '.join((BigWorld.wg_getShortDateFormat(record), BigWorld.wg_getShortTimeFormat(record)))


class RegularArenaFullNameItem(base.StatsItem):
    __slots__ = ()

    def _convert(self, record, reusable):
        arenaGuiType = reusable.common.arenaGuiType
        arenaType = reusable.common.arenaType
        if arenaGuiType == ARENA_GUI_TYPE.SORTIE:
            i18nKey = BATTLE_RESULTS.COMMON_BATTLETYPE_SORTIE
        elif arenaGuiType == ARENA_GUI_TYPE.RANDOM:
            i18nKey = _ARENA_TYPE_FORMAT.format(arenaType.getGamePlayName())
        else:
            i18nKey = _ARENA_TYPE_EXT_FORMAT.format(arenaGuiType)
        return makeArenaFullName(arenaType.getName(), i18nKey)


class FalloutArenaFullNameItem(base.StatsItem):
    __slots__ = ()

    def _convert(self, record, reusable):
        common = reusable.common
        arenaType = common.arenaType
        i18nKey = _ARENA_TYPE_EXT_FORMAT.format(common.arenaGuiType)
        if common.hasResourcePoints:
            i18nKey += '/resource'
        elif common.isMultiTeamMode:
            i18nKey += '/multiteam'
        return makeArenaFullName(arenaType.getName(), i18nKey)


class ArenaIconItem(base.StatsItem):
    __slots__ = ()

    def _convert(self, record, reusable):
        return reusable.common.getArenaIcon(_ARENA_ICON_PATH)


class ArenaDurationItem(base.StatsItem):
    __slots__ = ()

    def _convert(self, record, reusable):
        if record:
            converted = i18n.makeString(BATTLE_RESULTS.DETAILS_TIME_VALUE, int(record / 60), int(record % 60))
        else:
            converted = None
        return converted


class ArenaDurationVO(ArenaDurationItem):
    __slots__ = ()

    def _convert(self, record, reusable):
        return style.makeTimeStatsVO(self._field, super(ArenaDurationVO, self)._convert(record, reusable))


class PlayerKillingTimeVO(base.StatsItem):
    __slots__ = ()

    def _convert(self, record, reusable):
        info = reusable.personal.getLifeTimeInfo()
        if info.isKilled:
            minutes = int(info.lifeTime / 60)
            seconds = int(info.lifeTime % 60)
            converted = i18n.makeString(BATTLE_RESULTS.DETAILS_TIME_VALUE, minutes, seconds)
        else:
            converted = '-'
        return style.makeTimeStatsVO(self._field, converted)


class FinishResultMeta(base.DictMeta):
    __slots__ = ()

    def __init__(self, finishReasonLabel, shortResultLabel, fullResultLabel):
        meta = {finishReasonLabel: '',
         shortResultLabel: '',
         fullResultLabel: ''}
        auto = ((0, base.StatsItem(finishReasonLabel, 'finishReasonLabel')), (1, base.StatsItem(shortResultLabel, 'shortResultLabel')), (2, base.StatsItem(fullResultLabel, 'fullResultLabel')))
        super(FinishResultMeta, self).__init__(meta, auto)


class RegularFinishResultBlock(base.StatsBlock):
    __slots__ = ('finishReasonLabel', 'shortResultLabel', 'fullResultLabel')

    def __init__(self, meta = None, field = '', *path):
        super(RegularFinishResultBlock, self).__init__(meta, field, *path)
        self.finishReasonLabel = None
        self.shortResultLabel = None
        self.fullResultLabel = None
        return

    def setRecord(self, result, reusable):
        teamResult = reusable.getPersonalTeamResult()
        self.finishReasonLabel = makeRegularFinishResultLabel(reusable.common.finishReason, teamResult)
        self.shortResultLabel = teamResult
        self.fullResultLabel = _FULL_RESULT_LABEL.format(teamResult)


class FortBattleFinishResultBlock(RegularFinishResultBlock):
    __slots__ = ('finishReasonLabel', 'shortResultLabel', 'fullResultLabel')

    def setRecord(self, result, reusable):
        playerTeam = reusable.getPersonalTeam()
        if 'fortBuilding' in result:
            data = result['fortBuilding']
            buildTypeID = data.get('buildTypeID')
            buildTeam = data.get('buildTeam', 0)
            if buildTypeID is not None:
                buildingName = FortBuilding(typeID=buildTypeID).userName
            else:
                buildingName = ''
        else:
            buildTeam = 0
            buildingName = ''
        teamResult = reusable.getPersonalTeamResult()
        if teamResult == _TEAM_RESULT.DRAW:
            if buildTeam == playerTeam:
                teamResult = _TEAM_RESULT.WIN
            else:
                teamResult = _TEAM_RESULT.DEFEAT
        self.shortResultLabel = _FORT_BATTLE_SHORT_RESULT.format(teamResult)
        self.finishReasonLabel = makeFortBattleFinishResultLabel(teamResult, buildTeam == playerTeam, buildingName)
        self.fullResultLabel = _FULL_RESULT_LABEL.format(teamResult)
        return


class FalloutFinishResultBlock(RegularFinishResultBlock):
    __slots__ = ('finishReasonLabel', 'shortResultLabel', 'fullResultLabel')

    def setRecord(self, result, reusable):
        teamResult = reusable.getPersonalTeamResult()
        finishReason = reusable.common.finishReason
        if reusable.common.isMultiTeamMode:
            if teamResult in (_TEAM_RESULT.DEFEAT, _TEAM_RESULT.DRAW):
                teamResult = _TEAM_RESULT.ENDED
            falloutSubMode = 'multiteam'
        else:
            falloutSubMode = 'classic'
        resultTemplate = _FALLOUT_RESULT_LABEL.format(submode=falloutSubMode, status=teamResult)
        if teamResult not in (_TEAM_RESULT.DRAW, _TEAM_RESULT.ENDED):
            finishReasonStr = 'points'
            if finishReason == FINISH_REASON.WIN_POINTS_CAP:
                finishReasonStr = 'cap'
            elif finishReason == FINISH_REASON.EXTERMINATION:
                finishReasonStr = 'extermination'
            resultTemplate += '/' + finishReasonStr
        self.finishReasonLabel = i18n.makeString(resultTemplate)
        self.shortResultLabel = teamResult
        self.fullResultLabel = _FULL_RESULT_LABEL.format(teamResult)


class StrongholdBattleFinishResultBlock(RegularFinishResultBlock):
    __slots__ = ('finishReasonLabel', 'shortResultLabel', 'fullResultLabel')

    def setRecord(self, result, reusable):
        teamResult = reusable.getPersonalTeamResult()
        team = reusable.getPersonalTeam()
        winnerIfDraw = reusable.personal.avatar.winnerIfDraw
        if teamResult == _TEAM_RESULT.DRAW and winnerIfDraw:
            if team == winnerIfDraw:
                teamResult = _TEAM_RESULT.WIN
            else:
                teamResult = _TEAM_RESULT.DEFEAT
        self.finishReasonLabel = makeRegularFinishResultLabel(reusable.common.finishReason, teamResult)
        self.shortResultLabel = teamResult
        self.fullResultLabel = _FULL_RESULT_LABEL.format(teamResult)


class AllyTeamClanTitle(base.StatsItem):
    __slots__ = ()

    def _convert(self, value, reusable):
        return '{} [{}]'.format(BATTLE_RESULTS.TEAM_STATS_OWNTEAM, reusable.players.getFirstAllyClan(reusable.getPersonalTeam()).clanAbbrev)


class EnemyTeamClanTitle(base.StatsItem):
    __slots__ = ()

    def _convert(self, value, reusable):
        return '{} [{}]'.format(BATTLE_RESULTS.TEAM_STATS_ENEMYTEAM, reusable.players.getFirstEnemyClan(reusable.getPersonalTeam()).clanAbbrev)


class ClanInfoBlock(base.StatsBlock):
    __slots__ = ('clanDBID', 'clanAbbrev')

    def __init__(self, meta = None, field = '', *path):
        super(ClanInfoBlock, self).__init__(meta, field, *path)
        self.clanDBID = None
        self.clanAbbrev = None
        return

    def setRecord(self, record, reusable):
        if record is not None:
            self.clanDBID = record.clanDBID
            self.clanAbbrev = '[{}]'.format(record.clanAbbrev)
        return


class ClansInfoBlock(base.StatsBlock):
    __slots__ = ('allies', 'enemies')

    def __init__(self, meta = None, field = '', *path):
        super(ClansInfoBlock, self).__init__(meta, field, *path)
        self.allies = None
        self.enemies = None
        return

    def setRecord(self, record, reusable):
        team = reusable.getPersonalTeam()
        players = reusable.players
        self.allies = players.getFirstAllyClan(team)
        self.enemies = players.getFirstEnemyClan(team)


class RankChangesBlock(base.StatsBlock):
    __slots__ = ('state', 'linkage', 'title', 'description')

    def __init__(self, meta = None, field = '', *path):
        super(RankChangesBlock, self).__init__(meta, field, *path)
        self.state = None
        self.linkage = None
        self.title = None
        self.description = None
        return

    def setRecord(self, result, reusable):
        helper = RankInfoHelper(reusable)
        self.state = helper.makeStateLabel()
        self.linkage = 'RankedBattleSubTaskUI'
        self.title = helper.makeTitleLabel()
        self.description = helper.makeDescriptionLabel()


class RankedResultsBlockTitle(base.StatsItem):

    def _convert(self, value, reusable):
        helper = RankInfoHelper(reusable)
        return style.makeRankedResultsTitle(helper.makeTitleLabel())


class TotalFortResourceItem(base.StatsItem):
    __slots__ = ()

    def _convert(self, value, reusable):
        return style.makeTotalFortResourcesItem(reusable.personal.getFortTotalResourcesInfo().totalFortResource)


class TotalInfluencePointsItem(base.StatsItem):
    __slots__ = ()

    def _convert(self, value, reusable):
        info = reusable.personal.getFortTotalResourcesInfo()
        if info.totalInfluencePoints > 0:
            converted = style.makeTotalInfluencePointsItem(info.totalInfluencePoints)
        else:
            converted = ''
        return converted


class TeamsUiVisibility(base.StatsItem):

    def _convert(self, value, reusable):
        ui_visibility = 0
        if reusable.isSquadSupported:
            ui_visibility |= UI_VISIBILITY.SHOW_SQUAD
        return ui_visibility


class SortieTeamsUiVisibility(TeamsUiVisibility):

    def __init__(self, field, *path):
        super(SortieTeamsUiVisibility, self).__init__(field, *path)

    def _convert(self, value, reusable):
        ui_visibility = super(SortieTeamsUiVisibility, self)._convert(value, reusable)
        ui_visibility |= UI_VISIBILITY.SHOW_RESOURCES
        return ui_visibility