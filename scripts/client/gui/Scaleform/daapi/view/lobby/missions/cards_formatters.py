# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/missions/cards_formatters.py
from debug_utils import LOG_ERROR
from gui.Scaleform.genConsts.MISSIONS_ALIASES import MISSIONS_ALIASES
from gui.Scaleform.genConsts.TOOLTIPS_CONSTANTS import TOOLTIPS_CONSTANTS
from gui.Scaleform.locale.QUESTS import QUESTS
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.server_events import formatters
from gui.server_events.cond_formatters import CONDITION_ICON, FORMATTER_IDS, FormattableField, CONDITION_SIZE, getCondIconBySize
from gui.server_events.cond_formatters.formatters import ConditionsFormatter
from gui.server_events.cond_formatters.mixed_formatters import MissionBonusAndPostBattleCondFormatter, PersonalMissionConditionsFormatter
from gui.server_events.cond_formatters.tokens import TokensConditionFormatter
from gui.server_events.formatters import TOKEN_SIZES
from gui.shared.formatters import text_styles, icons
from gui.shared.utils.functions import makeTooltip
from helpers import i18n
MAX_ACHIEVEMENTS_IN_TOOLTIP = 5
CARD_FIELDS_FORMATTERS = {FORMATTER_IDS.SIMPLE_TITLE: formatters.minimizedTitleFormat,
 FORMATTER_IDS.CUMULATIVE: formatters.minimizedTitleCumulativeFormat,
 FORMATTER_IDS.COMPLEX: formatters.minimizedTitleComplexFormat,
 FORMATTER_IDS.RELATION: formatters.minimizedTitleRelationFormat,
 FORMATTER_IDS.DESCRIPTION: text_styles.main,
 FORMATTER_IDS.COMPLEX_RELATION: formatters.minimizedTitleComplexRelationFormat}
NORMAL_FORMATTERS = {FORMATTER_IDS.SIMPLE_TITLE: formatters.titleFormat,
 FORMATTER_IDS.CUMULATIVE: formatters.titleCumulativeFormat,
 FORMATTER_IDS.COMPLEX: formatters.titleComplexFormat,
 FORMATTER_IDS.RELATION: formatters.titleRelationFormat,
 FORMATTER_IDS.DESCRIPTION: text_styles.highlightText,
 FORMATTER_IDS.COMPLEX_RELATION: formatters.titleComplexRelationFormat}
MINIMIZED_FORMATTERS = {FORMATTER_IDS.SIMPLE_TITLE: formatters.minimizedTitleFormat,
 FORMATTER_IDS.CUMULATIVE: formatters.minimizedTitleCumulativeFormat,
 FORMATTER_IDS.COMPLEX: formatters.minimizedTitleComplexFormat,
 FORMATTER_IDS.RELATION: formatters.minimizedTitleRelationFormat,
 FORMATTER_IDS.DESCRIPTION: text_styles.main,
 FORMATTER_IDS.COMPLEX_RELATION: formatters.minimizedTitleComplexRelationFormat}

def _packNoGuiCondition(event):
    titleArgs = (i18n.makeString(QUESTS.DETAILS_CONDITIONS_TARGET_TITLE),)
    descrArgs = (event.getDescription(),)
    return formatters.packMissionIconCondition(FormattableField(FORMATTER_IDS.SIMPLE_TITLE, titleArgs), MISSIONS_ALIASES.NONE, FormattableField(FORMATTER_IDS.DESCRIPTION, descrArgs), CONDITION_ICON.FOLDER)


def _packProgress(preFormattedCondition):
    return {'maxValue': preFormattedCondition.total,
     'value': preFormattedCondition.current}


def _getTooltipData(conditionData):
    rendererLinkage = conditionData.get('data').get('rendererLinkage')
    if rendererLinkage == MISSIONS_ALIASES.ACHIEVEMENT_RENDERER:
        return _packAchievementsTooltipData(conditionData.get('data'))
    elif rendererLinkage == MISSIONS_ALIASES.VEHICLE_ITEM_RENDERER:
        return {'isSpecial': True,
         'tooltip': TOOLTIPS_CONSTANTS.MISSION_VEHICLE,
         'specialArgs': [conditionData.get('data')],
         'specialAlias': TOOLTIPS_CONSTANTS.MISSION_VEHICLE}
    elif rendererLinkage == MISSIONS_ALIASES.VEHICLE_TYPE_RENDERER:
        return {'isSpecial': True,
         'tooltip': TOOLTIPS_CONSTANTS.MISSION_VEHICLE_TYPE,
         'specialArgs': [conditionData.get('data')],
         'specialAlias': TOOLTIPS_CONSTANTS.MISSION_VEHICLE_TYPE}
    else:
        return None


def _packAchievementsTooltipData(data):
    achievementsNames = [ i18n.makeString(TOOLTIPS.MISSIONS_CONDITION_ACHIEVEMENT_PATTERN, achievement=item['label']) for item in data.get('list', []) ]
    header = i18n.makeString(TOOLTIPS.QUESTS_CONDITION_ACHIEVEMENT_HEADER)
    body = i18n.makeString(TOOLTIPS.QUESTS_CONDITION_ACHIEVEMENTS_DESCR) + '\n'
    achivementsCount = len(achievementsNames)
    if achivementsCount > MAX_ACHIEVEMENTS_IN_TOOLTIP:
        achievementsNames = achievementsNames[:MAX_ACHIEVEMENTS_IN_TOOLTIP]
        achievementsStr = '\n'.join(achievementsNames)
        others = '\n' + i18n.makeString(TOOLTIPS.QUESTS_CONDITION_ACHIEVEMENTS_OTHERS, count=achivementsCount - len(achievementsNames))
        body = '\n'.join((body, achievementsStr, others))
    else:
        achievementsNames = achievementsNames[:MAX_ACHIEVEMENTS_IN_TOOLTIP]
        achievementsStr = '\n'.join(achievementsNames)
        body = '\n'.join((body, achievementsStr))
    tooltip = makeTooltip(header, body)
    return {'tooltip': tooltip,
     'isSpecial': False,
     'specialArgs': []}


class CardBattleConditionsFormatters(MissionBonusAndPostBattleCondFormatter):
    """
    Formatter for 'bonus' and 'postbattle' conditions sections for mission card in missions view.
    Expand and mix all battle pre formatted conditions data in rows,
    then format rows in mission card specific format.
    Only one row of conditions is displayed in card,
    others are replaced by 'ALTERNATIVE' merged conditions renderer.
    Formatter slice and display only 3 first conditions in row,
    others are replaced by merged 'ADDITIONAL' conditions renderer.
    """
    MAX_CONDITIONS_IN_CARD = 3
    MAX_DESC_LINES = 3
    ALT_DESCR_LINES = 2

    def __init__(self):
        self._formatters = CARD_FIELDS_FORMATTERS
        super(CardBattleConditionsFormatters, self).__init__()

    def format(self, event):
        components = []
        maxDescLines = self.MAX_DESC_LINES
        if not event.isGuiDisabled():
            result = super(CardBattleConditionsFormatters, self).format(event)
            for idx, condList in enumerate(result):
                if idx == 0:
                    if len(condList) > self.MAX_CONDITIONS_IN_CARD:
                        maxDescLines = self.ALT_DESCR_LINES
                        components.append(self._packConditions(condList[:self.MAX_CONDITIONS_IN_CARD], maxDescLines))
                        components.append(self._packSeparator(QUESTS.DETAILS_CONDITIONS_ADDITIONAL))
                    else:
                        components.append(self._packConditions(condList, maxDescLines))

        else:
            components.append(self._packConditions([_packNoGuiCondition(event)]))
        return components

    def _getFormattedField(self, formattableField):
        formatter = self._formatters.get(formattableField.formatterID)
        return formatter(*formattableField.args)

    @classmethod
    def _packSeparator(cls, key):
        return {'linkage': MISSIONS_ALIASES.ALTERNATIVE_CONDITIONS_SEPARATOR,
         'linkageBig': MISSIONS_ALIASES.ALTERNATIVE_CONDITIONS_SEPARATOR,
         'rendererLinkage': None,
         'data': {'label': '%s %s' % (icons.makeImageTag(RES_ICONS.MAPS_ICONS_LIBRARY_STORE_CONDITION_ON, 16, 16, -2), text_styles.main(i18n.makeString(key))),
                  'tooltip': i18n.makeString(TOOLTIPS.DETAILS_CONDITIONS_ADDITIONAL)},
         'isDetailed': False}

    def _packCondition(self, preFormattedCondition, maxDescLines = MAX_DESC_LINES):
        state = preFormattedCondition.progressType
        tooltipData = None
        if preFormattedCondition.conditionData is not None:
            tooltipData = _getTooltipData(preFormattedCondition.conditionData)
        return {'icon': getCondIconBySize(CONDITION_SIZE.MINIMIZED, preFormattedCondition.iconKey),
         'title': self._getFormattedField(preFormattedCondition.titleData),
         'description': self._getFormattedField(preFormattedCondition.descrData),
         'progress': _packProgress(preFormattedCondition),
         'state': state,
         'tooltipData': tooltipData,
         'conditionData': preFormattedCondition.conditionData,
         'maxDescLines': maxDescLines}

    def _packConditions(self, preFormattedConditions, maxDescLines = MAX_DESC_LINES):
        result = []
        for cond in preFormattedConditions:
            result.append(self._packCondition(cond, maxDescLines))

        return {'linkage': MISSIONS_ALIASES.ANG_GROUP_LINKAGE,
         'linkageBig': MISSIONS_ALIASES.ANG_GROUP_BIG_LINKAGE,
         'rendererLinkage': MISSIONS_ALIASES.MINIMIZED_BATTLE_CONDITION,
         'data': result,
         'isDetailed': False}


class DetailedCardBattleConditionsFormatters(MissionBonusAndPostBattleCondFormatter):
    """
    Formatter for 'bonus' and 'postbattle' conditions sections for detailed mission card in detailed missions view.
    Expand and mix all battle pre formatted conditions data in rows,
    then format rows in mission card specific format.
    Only two rows of conditions is displayed in card, UX requirement.
    Others are not displayed. SSE should control quests xml. Only one 'OR' section is supported by GUI.
    There are only 6 conditions are supported by GUI.
    For example: all 6 in 'AND' section, UX requirement.
    3 in first 'AND' row and 3 in second 'AND' row inside 'OR' section - 6 total
    """
    MAX_CONDITIONS_IN_CARD = 6
    MAX_CONDITIONS_IN_ROW = 3
    MAX_OR_SECTIONS = 2
    MAX_LINES_IN_DESCR = 3
    MIN_LINES_IN_DESCR = 2

    def __init__(self):
        self._formatters = {CONDITION_SIZE.NORMAL: NORMAL_FORMATTERS,
         CONDITION_SIZE.MINIMIZED: MINIMIZED_FORMATTERS}
        super(DetailedCardBattleConditionsFormatters, self).__init__()

    def format(self, event):
        if not event.isGuiDisabled():
            result = super(DetailedCardBattleConditionsFormatters, self).format(event)
            if len(result) < self.MAX_OR_SECTIONS:
                return self.__andFormat(result)
            return self.__orFormat(result)
        return [self._packConditions(CONDITION_SIZE.NORMAL, [_packNoGuiCondition(event)])]

    def _packConditions(self, size, conditions):
        if len(conditions) > self.MAX_CONDITIONS_IN_CARD:
            conditions = conditions[:self.MAX_CONDITIONS_IN_CARD]
            LOG_ERROR('Wrong quest xml. Conditions count limit exceeded. SSE bug.')
        result = []
        for cond in conditions:
            result.append(self._packCondition(size, cond))

        linkage = MISSIONS_ALIASES.BATTLE_CONDITION
        contLinkageBig = MISSIONS_ALIASES.ANG_GROUP_BIG_LINKAGE
        if size == CONDITION_SIZE.MINIMIZED:
            linkage = MISSIONS_ALIASES.BATTLE_CONDITION_SMALL
            contLinkageBig = MISSIONS_ALIASES.ANG_GROUP_DETAILED_LINKAGE
        return {'linkage': MISSIONS_ALIASES.ANG_GROUP_DETAILED_LINKAGE,
         'linkageBig': contLinkageBig,
         'rendererLinkage': linkage,
         'data': result,
         'isDetailed': True}

    def _packCondition(self, size, preFormattedCondition):
        iconKey = preFormattedCondition.iconKey
        progress = _packProgress(preFormattedCondition)
        return {'icon': getCondIconBySize(size, iconKey),
         'title': self._getFormattedField(size, preFormattedCondition.titleData),
         'description': self._getFormattedField(size, preFormattedCondition.descrData),
         'progress': progress,
         'state': preFormattedCondition.progressType,
         'conditionData': preFormattedCondition.conditionData,
         'maxDescLines': self.MIN_LINES_IN_DESCR if size == CONDITION_SIZE.MINIMIZED else self.MAX_LINES_IN_DESCR}

    @classmethod
    def _packSeparator(cls, key):
        return {'linkage': MISSIONS_ALIASES.OR_CONDITIONS_SEPARATOR,
         'linkageBig': MISSIONS_ALIASES.OR_CONDITIONS_SEPARATOR,
         'rendererLinkage': None,
         'data': {'label': text_styles.warning(i18n.makeString(key).upper())},
         'isDetailed': True}

    def _getFormattedField(self, size, formattableField):
        formatter = self._formatters[size].get(formattableField.formatterID, None)
        if formatter and callable(formatter):
            return formatter(*formattableField.args)
        else:
            return

    def __andFormat(self, result):
        components = []
        for idx, condList in enumerate(result):
            size = CONDITION_SIZE.MINIMIZED if len(condList) > self.MAX_CONDITIONS_IN_ROW else CONDITION_SIZE.NORMAL
            components.append(self._packConditions(size, condList))

        return components

    def __orFormat(self, result):
        components = []
        for idx, condList in enumerate(result):
            if idx > 0:
                components.append(self._packSeparator(QUESTS.DETAILS_GROUPS_OR))
            if len(condList) > self.MAX_CONDITIONS_IN_ROW:
                condList = condList[:self.MAX_CONDITIONS_IN_ROW]
                LOG_ERROR("Wrong quest xml. Conditions count limit in 'or' section exceeded. SSE bug.")
            components.append(self._packConditions(CONDITION_SIZE.MINIMIZED, condList))

        return components


class CardTokenConditionFormatter(ConditionsFormatter):
    """
    Formatter for 'token' conditions sections for mission card in missions view.
    """
    MAX_TOKENS_COUNT = 3

    def __init__(self):
        super(CardTokenConditionFormatter, self).__init__()
        self.tokensCondFormatter = TokensConditionFormatter()

    def format(self, event):
        if not event.isGuiDisabled():
            preFormattedConditions = self.getPreformattedConditions(event)
            if len(preFormattedConditions) > self.MAX_TOKENS_COUNT:
                preFormattedConditions = preFormattedConditions[:self.MAX_TOKENS_COUNT]
                LOG_ERROR('Wrong quest xml. Tokens types limit exceeded in account requirement section. SSE bug.')
            return [self._packConditions(preFormattedConditions)]
        else:
            return [self.__packConditionFromDescription(event)]

    def getPreformattedConditions(self, event):
        return self.tokensCondFormatter.format(event.accountReqs, event)

    @classmethod
    def _getLabel(cls, preFormattedCondition):
        return text_styles.neutral(preFormattedCondition.title)

    @classmethod
    def _getIconData(cls, preFormattedCondition):
        return {'imgSrc': preFormattedCondition.getImage(TOKEN_SIZES.MEDIUM),
         'isNormalSize': True}

    @classmethod
    def _packBattleCondition(cls, preFormattedCondition):
        return {'icon': getCondIconBySize(CONDITION_SIZE.MINIMIZED, preFormattedCondition.iconKey),
         'title': formatters.minimizedTitleFormat(*preFormattedCondition.titleData.args),
         'description': text_styles.main(*preFormattedCondition.descrData.args),
         'state': preFormattedCondition.progressType}

    def _packConditions(self, preFormattedConditions):
        result = []
        if len(preFormattedConditions) < self.MAX_TOKENS_COUNT:
            formatter = self._packFullCondition
        else:
            formatter = self.__packSimplifiedCondition
        for cond in preFormattedConditions:
            result.append(formatter(cond, popoverEnable=False))

        return {'linkage': MISSIONS_ALIASES.ANG_GROUP_LINKAGE,
         'linkageBig': MISSIONS_ALIASES.ANG_GROUP_BIG_LINKAGE,
         'rendererLinkage': MISSIONS_ALIASES.MINIMIZED_TOKEN_CONDITION,
         'data': result,
         'isDetailed': False}

    def _packFullCondition(self, preFormattedCondition, popoverEnable):
        data = self.__packSimplifiedCondition(preFormattedCondition, popoverEnable)
        data.update({'titleText': self._getLabel(preFormattedCondition)})
        return data

    def __packSimplifiedCondition(self, preFormattedCondition, popoverEnable):
        data = {'tokenId': preFormattedCondition.tokenID,
         'questId': preFormattedCondition.eventID,
         'countText': preFormattedCondition.getCounterText(),
         'popoverEnable': popoverEnable}
        data.update(self._getIconData(preFormattedCondition))
        return data

    def __packConditionFromDescription(self, event):
        return {'linkage': MISSIONS_ALIASES.ANG_GROUP_LINKAGE,
         'linkageBig': MISSIONS_ALIASES.ANG_GROUP_BIG_LINKAGE,
         'rendererLinkage': self._getRendererLinkage(),
         'data': [self._packBattleCondition(_packNoGuiCondition(event))],
         'isDetailed': self._getIsDetailed()}

    def _getRendererLinkage(self):
        return MISSIONS_ALIASES.MINIMIZED_BATTLE_CONDITION

    def _getIsDetailed(self):
        return False


class DetailedCardTokenConditionFormatter(CardTokenConditionFormatter):
    """
    Formatter for 'token' conditions sections for detailed mission card in detailed missions view.
    """

    @classmethod
    def _packBattleCondition(cls, preFormattedCondition):
        return {'icon': getCondIconBySize(CONDITION_SIZE.NORMAL, preFormattedCondition.iconKey),
         'title': formatters.titleFormat(*preFormattedCondition.titleData.args),
         'description': text_styles.highlightText(*preFormattedCondition.descrData.args),
         'state': preFormattedCondition.progressType}

    @classmethod
    def _getLabel(cls, preFormattedCondition):
        return text_styles.stats(preFormattedCondition.title)

    @classmethod
    def _getIconData(cls, preFormattedCondition):
        return {'imgSrc': preFormattedCondition.getImage(TOKEN_SIZES.BIG),
         'isNormalSize': False}

    def _packConditions(self, preFormattedConditions):
        result = []
        for cond in preFormattedConditions:
            result.append(self._packFullCondition(cond, popoverEnable=True))

        return {'linkage': MISSIONS_ALIASES.ANG_GROUP_DETAILED_LINKAGE,
         'linkageBig': MISSIONS_ALIASES.TOKENS_GROUP_BIG_LINKAGE,
         'rendererLinkage': MISSIONS_ALIASES.TOKEN_CONDITION,
         'data': result,
         'isDetailed': True}

    def _getRendererLinkage(self):
        return MISSIONS_ALIASES.BATTLE_CONDITION

    def _getIsDetailed(self):
        return True


class PMCardConditionsFormatter(PersonalMissionConditionsFormatter):
    """
    Conditions formatter for personal mission, which are displayed in detailed personal mission's view
    """

    def format(self, event, isMain = None):
        results = super(PMCardConditionsFormatter, self).format(event, isMain)
        if isMain is not None and not isMain and event.isMainCompleted():
            results.insert(0, self.__packAdditionalCondition(self._isConditionBlockAvailable(event, isMain)))
        return results

    def _packCondition(self, preFormattedCondition, isAvailable, isInOrGroup):
        return {'icon': getCondIconBySize(CONDITION_SIZE.NORMAL, preFormattedCondition.iconKey),
         'title': self._getFormattedField(preFormattedCondition.titleData),
         'description': self._getFormattedField(preFormattedCondition.descrData),
         'isEnabled': isAvailable,
         'isInOrGroup': isInOrGroup}

    def __packAdditionalCondition(self, isAvailable):
        return {'icon': getCondIconBySize(CONDITION_SIZE.NORMAL, CONDITION_ICON.FOLDER),
         'title': self._formatters[FORMATTER_IDS.SIMPLE_TITLE](QUESTS.DETAILS_CONDITIONS_ADDITIONAL_TITLE),
         'description': '',
         'isEnabled': isAvailable}