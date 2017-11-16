# Embedded file name: scripts/client/gui/server_events/cond_formatters/mixed_formatters.py
from collections import namedtuple
from gui.Scaleform.genConsts.MISSIONS_ALIASES import MISSIONS_ALIASES
from gui.Scaleform.locale.QUESTS import QUESTS
from gui.server_events import formatters
from gui.server_events.cond_formatters import FormattableField, FORMATTER_IDS, CONDITION_ICON, BATTLE_RESULTS_KEYS
from gui.server_events.cond_formatters import postbattle
from gui.server_events.cond_formatters.bonus import MissionsBonusConditionsFormatter, BattlesCountFormatter
from gui.server_events.cond_formatters.formatters import ConditionsFormatter
from gui.server_events.cond_formatters.postbattle import GroupResult
from gui.server_events.cond_formatters.prebattle import PersonalMissionsVehicleConditionsFormatter
from gui.server_events.formatters import PreFormattedCondition
from helpers import i18n

def _packPlayBattleCondition():
    titleArgs = (i18n.makeString(QUESTS.DETAILS_CONDITIONS_PLAYBATTLE_TITLE),)
    descrArgs = (i18n.makeString(QUESTS.MISSIONDETAILS_CONDITIONS_PLAYBATTLE),)
    return formatters.packMissionIconCondition(FormattableField(FORMATTER_IDS.SIMPLE_TITLE, titleArgs), MISSIONS_ALIASES.NONE, FormattableField(FORMATTER_IDS.DESCRIPTION, descrArgs), CONDITION_ICON.BATTLES)


class MissionBonusAndPostBattleCondFormatter(ConditionsFormatter):
    """
    Formatter for 'bonus' and 'postbattle' conditions sections
    Expand and mix all battle pre formatted conditions data in rows
    All 'AND' conditions collected in one row
    'OR' conditions expand in different rows.
    results represent 'OR' list of rows with 'AND' conditions
    for example: (damage vehicle and win) or (kill vehicle and survive) looks like
    [
        [veh damage data, win data],
        [veh kill data , survive data]
    ]
    """

    def __init__(self):
        super(MissionBonusAndPostBattleCondFormatter, self).__init__()
        self.bonusCondFormatter = MissionsBonusConditionsFormatter()
        self.postBattleCondFormatter = postbattle.MissionsPostBattleConditionsFormatter()

    def format(self, event):
        result = []
        bonusConditions = self.bonusCondFormatter.format(event.bonusCond, event)
        postBattleConditions = self.postBattleCondFormatter.format(event.postBattleCond, event)
        battleCountCondition = event.bonusCond.getConditions().find('battles')
        for pCondGroup in postBattleConditions:
            for bCondGroup in bonusConditions:
                if battleCountCondition is not None:
                    conditions = []
                    conditions.extend(pCondGroup)
                    conditions.extend(bCondGroup)
                    conditions.extend(BattlesCountFormatter(bool(pCondGroup)).format(battleCountCondition, event))
                else:
                    conditions = pCondGroup + bCondGroup
                if not conditions:
                    conditions.append(_packPlayBattleCondition())
                result.append(conditions)

        return result

    @classmethod
    def _packSeparator(cls, key):
        raise NotImplementedError


PERSONAL_MISSSIONS_FORMATTERS = {FORMATTER_IDS.SIMPLE_TITLE: formatters.simpleFormat,
 FORMATTER_IDS.CUMULATIVE: formatters.personalTitleCumulativeFormat,
 FORMATTER_IDS.COMPLEX: formatters.personalTitleCumulativeFormat,
 FORMATTER_IDS.RELATION: formatters.personalTitleRelationFormat,
 FORMATTER_IDS.DESCRIPTION: formatters.simpleFormat,
 FORMATTER_IDS.COMPLEX_RELATION: formatters.personalTitleComplexRelationFormat}
KEYS_ORDER = ('vehicleDamage', 'vehicleKills', 'vehicleStun', 'achievements', 'crits', 'multiStunEvent', 'top', 'results', 'damageDealt', 'kills', 'isAnyOurCrittedInnerModules', 'isNotSpotted', 'unitResults', 'clanKills', 'installedItem', 'correspondedCamouflage', 'win', 'isAlive')

def getKeySortOrder(key):
    if key in KEYS_ORDER:
        return KEYS_ORDER.index(key)
    if key in BATTLE_RESULTS_KEYS:
        return KEYS_ORDER.index('results')
    return -1


def sortConditionsFunc(aData, bData):
    aCondData, _, aInOrGroup = aData
    bCondData, _, bInOrGroup = bData
    res = cmp(aInOrGroup, bInOrGroup)
    if res:
        return res
    return cmp(getKeySortOrder(aCondData.sortKey), getKeySortOrder(bCondData.sortKey))


class PersonalMissionConditionsFormatter(ConditionsFormatter):
    """
    Conditions formatter for personal mission, which are displayed in detailed personal mission's view
    """

    def __init__(self):
        super(PersonalMissionConditionsFormatter, self).__init__()
        self._formatters = PERSONAL_MISSSIONS_FORMATTERS
        self.postBattleCondFormatter = postbattle.PersonalMissionsPostBattleConditionsFormatter()
        self.vehicleConditionsFormatter = PersonalMissionsVehicleConditionsFormatter()

    def format(self, event, isMain = None):
        conditionsData = []
        isAvailable = self._isConditionBlockAvailable(event, isMain)
        postBattleResult = self.postBattleCondFormatter.format(event.getPostBattleConditions(isMain), event)
        vehicleResult = self.vehicleConditionsFormatter.format(event.getVehicleRequirements(isMain), event)
        conditionsData.extend(self._packConditions(vehicleResult, isAvailable))
        conditionsData.extend(self._packConditions(postBattleResult, isAvailable))
        conditionsData = sorted(conditionsData, cmp=sortConditionsFunc)
        results = [ self._packCondition(*c) for c in conditionsData ]
        return results

    @classmethod
    def _isConditionBlockAvailable(cla, event, isMain):
        isAvailable = event.isUnlocked()
        if isMain:
            isAvailable = isAvailable and not event.isMainCompleted()
        elif not isMain:
            isAvailable = isAvailable and not event.isFullCompleted()
        return isAvailable

    def _getFormattedField(self, formattableField):
        formatter = self._formatters.get(formattableField.formatterID)
        return formatter(*formattableField.args)

    def _packConditions(self, groupResult, isAvailable):
        result = []
        if isinstance(groupResult, list):
            for res in groupResult:
                if isinstance(res, PreFormattedCondition):
                    result.append((res, isAvailable, False))
                else:
                    result.extend(self._packConditions(res, isAvailable))

        elif isinstance(groupResult, GroupResult):
            for res in groupResult.results:
                if isinstance(res, PreFormattedCondition):
                    result.append((res, isAvailable, groupResult.isOrGroup))
                else:
                    result.extend(self._packConditions(res, isAvailable))

        return result


class StringPersonalMissionConditionsFormatter(PersonalMissionConditionsFormatter):
    _CONDITION = namedtuple('_CONDITION', ['text', 'isInOrGroup'])

    def format(self, event, isMain = None):
        results = super(StringPersonalMissionConditionsFormatter, self).format(event, isMain)
        orConditions = filter(lambda q: q.isInOrGroup, results)
        andConditions = filter(lambda q: not q.isInOrGroup, results)
        andResult = ''
        for c in andConditions:
            andResult += '%s %s\n' % (i18n.makeString(QUESTS.QUEST_CONDITION_DOT), c.text)

        orTexts = [ '%s %s' % (i18n.makeString(QUESTS.QUEST_CONDITION_DOT), c.text) for c in orConditions ]
        orResult = ('\n%s\n' % i18n.makeString(QUESTS.QUEST_CONDITION_OR)).join(orTexts)
        if orResult:
            return '%s\n%s' % (orResult, andResult)
        return andResult

    def _packCondition(self, preFormattedCondition, isAvailable, isInOrGroup):
        title = self._getFormattedField(preFormattedCondition.titleData)
        description = self._getFormattedField(preFormattedCondition.descrData)
        if description:
            text = description
        else:
            text = title
        return self._CONDITION(text, isInOrGroup)