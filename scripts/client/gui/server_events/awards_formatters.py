# Embedded file name: scripts/client/gui/server_events/awards_formatters.py
from collections import namedtuple
from debug_utils import LOG_WARNING
from gui.Scaleform.locale.NY import NY
from helpers.i18n import makeString
from gui.Scaleform.genConsts.SLOT_HIGHLIGHT_TYPES import SLOT_HIGHLIGHT_TYPES
from gui.Scaleform.genConsts.TOOLTIPS_CONSTANTS import TOOLTIPS_CONSTANTS
from gui.Scaleform.locale.QUESTS import QUESTS
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.server_events.formatters import parseComplexToken, TOKEN_SIZES
from gui.shared.formatters import text_styles
from gui.shared.gui_items import GUI_ITEM_TYPE, GUI_ITEM_TYPE_INDICES, getItemIconName
from gui.shared.gui_items.Tankman import getRoleUserName
from gui.shared.money import Currency
from gui.shared.utils.functions import makeTooltip
from gui.shared.utils.requesters import REQ_CRITERIA
from helpers import time_utils, i18n, dependency
from shared_utils import CONST_CONTAINER, findFirst
from skeletons.gui.server_events import IEventsCache
from skeletons.gui.customization import ICustomizationService
from skeletons.new_year import INewYearController

class AWARDS_SIZES(CONST_CONTAINER):
    SMALL = 'small'
    BIG = 'big'


class COMPLETION_TOKENS_SIZES(CONST_CONTAINER):
    SMALL = 'small'
    BIG = 'big'
    HUGE = 'huge'


class LABEL_ALIGN(CONST_CONTAINER):
    RIGHT = 'right'
    CENTER = 'center'


AWARD_IMAGES = {AWARDS_SIZES.SMALL: {Currency.CREDITS: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_CREDITS,
                      Currency.GOLD: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_GOLD,
                      Currency.CRYSTAL: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_CRYSTAL,
                      'creditsFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_CREDITS,
                      'freeXP': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_FREEEXP,
                      'freeXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_FREEEXP,
                      'tankmenXP': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_TANKMENXP,
                      'tankmenXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_TANKMENXP,
                      'xp': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_EXP,
                      'xpFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_EXP,
                      'dailyXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_SMALL_FREEEXP},
 AWARDS_SIZES.BIG: {Currency.CREDITS: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_CREDITS,
                    Currency.GOLD: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_GOLD,
                    Currency.CRYSTAL: RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_CRYSTAL,
                    'creditsFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_CREDITS,
                    'freeXP': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_FREEXP,
                    'freeXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_FREEXP,
                    'tankmenXP': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_TANKMENXP,
                    'tankmenXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_TANKMENXP,
                    'xp': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_EXP,
                    'xpFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_EXP,
                    'dailyXPFactor': RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_BIG_FREEXP}}

def _getMultiplierFormatter(formatter):

    def wrapper(text):
        return formatter('x{}'.format(text))

    return wrapper


TEXT_FORMATTERS = {Currency.CREDITS: text_styles.credits,
 Currency.GOLD: text_styles.gold,
 Currency.CRYSTAL: text_styles.crystal,
 'creditsFactor': _getMultiplierFormatter(text_styles.credits),
 'freeXP': text_styles.expText,
 'freeXPFactor': _getMultiplierFormatter(text_styles.expText),
 'tankmenXP': text_styles.expText,
 'tankmenXPFactor': _getMultiplierFormatter(text_styles.expText),
 'xp': text_styles.expText,
 'xpFactor': _getMultiplierFormatter(text_styles.expText),
 'dailyXPFactor': _getMultiplierFormatter(text_styles.expText)}
TEXT_ALIGNS = {'creditsFactor': LABEL_ALIGN.RIGHT,
 'freeXPFactor': LABEL_ALIGN.RIGHT,
 'tankmenXPFactor': LABEL_ALIGN.RIGHT,
 'dailyXPFactor': LABEL_ALIGN.RIGHT,
 'xpFactor': LABEL_ALIGN.RIGHT}

def getDefaultFormattersMap():
    simpleBonusFormatter = SimpleBonusFormatter()
    tokenBonusFormatter = NY18BoxFormatter()
    return {'strBonus': simpleBonusFormatter,
     Currency.GOLD: simpleBonusFormatter,
     Currency.CREDITS: simpleBonusFormatter,
     Currency.CRYSTAL: simpleBonusFormatter,
     'freeXP': simpleBonusFormatter,
     'xp': simpleBonusFormatter,
     'tankmenXP': simpleBonusFormatter,
     'xpFactor': simpleBonusFormatter,
     'creditsFactor': simpleBonusFormatter,
     'freeXPFactor': simpleBonusFormatter,
     'tankmenXPFactor': simpleBonusFormatter,
     'dailyXPFactor': simpleBonusFormatter,
     'premium': PremiumDaysBonusFormatter(),
     'vehicles': VehiclesBonusFormatter(),
     'meta': simpleBonusFormatter,
     'tokens': tokenBonusFormatter,
     'tankwomanBonus': TankwomanBonusFormatter(),
     'battleToken': tokenBonusFormatter,
     'tankmen': TankmenBonusFormatter(),
     'customizations': CustomizationsBonusFormatter(),
     'goodies': GoodiesBonusFormatter(),
     'items': ItemsBonusFormatter(),
     'dossier': DossierBonusFormatter()}


def getMisssionsFormattersMap():
    countableIntegralBonusFormatter = CountableIntegralBonusFormatter()
    mapping = getDefaultFormattersMap()
    mapping.update({'slots': countableIntegralBonusFormatter,
     'berths': countableIntegralBonusFormatter})
    return mapping


def getEventBoardsFormattersMap():
    countableIntegralBonusFormatter = CountableIntegralBonusFormatter()
    mapping = getDefaultFormattersMap()
    mapping.update({'dossier': EventBoardsDossierBonusFormatter(),
     'badgesGroup': BadgesGroupBonusFormatter(),
     'slots': countableIntegralBonusFormatter,
     'berths': countableIntegralBonusFormatter})
    return mapping


def getDefaultAwardFormatter():
    return AwardsPacker(getDefaultFormattersMap())


def getMissionAwardPacker():
    return AwardsPacker(getMisssionsFormattersMap())


def getEventBoardsAwardPacker():
    return AwardsPacker(getEventBoardsFormattersMap())


def getPersonalMissionAwardPacker():
    mapping = getDefaultFormattersMap()
    mapping.update({'completionTokens': CompletionTokensBonusFormatter(),
     'freeTokens': FreeTokensBonusFormatter(),
     'slots': CountableIntegralBonusFormatter()})
    return AwardsPacker(mapping)


def getOperationPacker():
    mapping = getDefaultFormattersMap()
    mapping.update({'customizations': OperationCustomizationsBonusFormatter(),
     'battleToken': CustomizationUnlockFormatter()})
    return AwardsPacker(mapping)


def formatCountLabel(count):
    if count > 1:
        return 'x{}'.format(count)
    return ''


_PreformattedBonus = namedtuple('_PreformattedBonus', 'bonusName, label userName images tooltip labelFormatter areTokensPawned specialArgs specialAlias isSpecial isCompensation align highlightType overlayType')

class PreformattedBonus(_PreformattedBonus):

    def getImage(self, size):
        return self.images.get(size, '')

    def getFormattedLabel(self, formatter = None):
        formatter = formatter or self.labelFormatter
        if formatter:
            return formatter(self.label)
        return self.label


PreformattedBonus.__new__.__defaults__ = (None,
 None,
 None,
 None,
 None,
 None,
 False,
 None,
 None,
 False,
 False,
 LABEL_ALIGN.CENTER,
 None,
 None)

class QuestsBonusComposer(object):

    def __init__(self, awardsFormatter = None):
        self.__bonusFormatter = awardsFormatter or getMissionAwardPacker()

    def getPreformattedBonuses(self, bonuses):
        return self.__bonusFormatter.format(bonuses)

    def getFormattedBonuses(self, bonuses, size = AWARDS_SIZES.SMALL):
        preformattedBonuses = self.getPreformattedBonuses(bonuses)
        return self._packBonuses(preformattedBonuses, size)

    def _packBonuses(self, preformattedBonuses, size):
        result = []
        for b in preformattedBonuses:
            result.append(self._packBonus(b, size))

        return result

    def _packBonus(self, bonus, size = AWARDS_SIZES.SMALL):
        return {'label': bonus.getFormattedLabel(),
         'imgSource': bonus.getImage(size),
         'tooltip': bonus.tooltip,
         'isSpecial': bonus.isSpecial,
         'specialAlias': bonus.specialAlias,
         'specialArgs': bonus.specialArgs,
         'align': bonus.align}


class AwardsPacker(object):

    def __init__(self, formatters = None):
        self.__formatters = formatters or {}

    def format(self, bonuses):
        preformattedBonuses = []
        for b in bonuses:
            if b.isShowInGUI():
                formatter = self._getBonusFormatter(b.getName())
                if formatter:
                    preformattedBonuses.extend(formatter.format(b))

        return preformattedBonuses

    def getFormatters(self):
        return self.__formatters

    def _getBonusFormatter(self, bonusName):
        return self.__formatters.get(bonusName)


class AwardFormatter(object):

    def format(self, bonus):
        return self._format(bonus)

    def _format(self, bonus):
        return None


class SimpleBonusFormatter(AwardFormatter):

    def _format(self, bonus):
        return [PreformattedBonus(bonusName=bonus.getName(), label=self._getLabel(bonus), userName=self._getUserName(bonus), labelFormatter=self._getLabelFormatter(bonus), images=self._getImages(bonus), tooltip=bonus.getTooltip(), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus))]

    @classmethod
    def _getUserName(cls, bonus):
        return i18n.makeString(QUESTS.getBonusName(bonus.getName()))

    @classmethod
    def _getLabel(cls, bonus):
        return bonus.formatValue()

    @classmethod
    def _getLabelFormatter(cls, bonus):
        return TEXT_FORMATTERS.get(bonus.getName(), text_styles.stats)

    @classmethod
    def _getLabelAlign(cls, bonus):
        return TEXT_ALIGNS.get(bonus.getName(), LABEL_ALIGN.CENTER)

    @classmethod
    def _getImages(cls, bonus):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = AWARD_IMAGES.get(size, {}).get(bonus.getName())

        return result

    @classmethod
    def _isCompensation(cls, bonus):
        return bonus.isCompensation()


class CountableIntegralBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        return [PreformattedBonus(bonusName=bonus.getName(), label=formatCountLabel(bonus.getValue()), userName=self._getUserName(bonus), labelFormatter=self._getLabelFormatter(bonus), images=self._getImages(bonus), tooltip=bonus.getTooltip(), align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus))]

    @classmethod
    def _getLabelFormatter(cls, bonus):
        return text_styles.stats

    @classmethod
    def _getImages(cls, bonus):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, bonus.getName())

        return result


class CompletionTokensBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        uniqueName = self._getUniqueName(bonus)
        return [PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(uniqueName), label=formatCountLabel(bonus.getCount()), images=self._getImages(uniqueName), tooltip=self._getTooltip(uniqueName), labelFormatter=self._getLabelFormatter(bonus), align=LABEL_ALIGN.RIGHT)]

    @classmethod
    def _getUserName(cls, nameID):
        return i18n.makeString(QUESTS.getBonusName(nameID))

    @classmethod
    def _getImages(cls, imageID):
        result = {}
        for size in COMPLETION_TOKENS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, imageID)

        return result

    @classmethod
    def _getTooltip(cls, tooltipID):
        header = i18n.makeString(TOOLTIPS.getAwardHeader(tooltipID))
        body = i18n.makeString(TOOLTIPS.getAwardBody(tooltipID))
        if header or body:
            return makeTooltip(header or None, body or None)
        else:
            return ''

    @classmethod
    def _getUniqueName(cls, bonus):
        context = bonus.getContext()
        operationID = context['operationID']
        chainID = context['chainID']
        return '%s_%s_%s' % (bonus.getName(), operationID, chainID)


class FreeTokensBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        areTokensPawned = bonus.areTokensPawned()
        if areTokensPawned:
            specialAlias = TOOLTIPS_CONSTANTS.FREE_SHEET_USED
            specialArgs = []
        else:
            specialAlias = TOOLTIPS_CONSTANTS.FREE_SHEET
            specialArgs = []
        return [PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(bonus), label=formatCountLabel(bonus.getCount()), images=self._getImages(bonus.getName()), labelFormatter=self._getLabelFormatter(bonus), align=LABEL_ALIGN.RIGHT, isCompensation=bonus.isCompensation(), isSpecial=True, specialAlias=specialAlias, specialArgs=specialArgs, areTokensPawned=areTokensPawned)]

    @classmethod
    def _getImages(cls, imageID):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, imageID)

        return result


class PremiumDaysBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        return [PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(bonus), images=self._getImages(bonus), tooltip=bonus.getTooltip(), isCompensation=self._isCompensation(bonus))]

    @classmethod
    def _getImages(cls, bonus):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getPremiumDaysAwardIcon(size, bonus.getValue())

        return result


class TokenBonusFormatter(SimpleBonusFormatter):
    eventsCache = dependency.descriptor(IEventsCache)

    def _format(self, bonus):
        result = []
        for tokenID, token in bonus.getTokens().iteritems():
            complexToken = parseComplexToken(tokenID)
            if complexToken.isDisplayable:
                userName = self._getUserName(complexToken.styleID)
                tooltip = makeTooltip(i18n.makeString(TOOLTIPS.QUESTS_BONUSES_TOKEN_HEADER, userName=userName), i18n.makeString(TOOLTIPS.QUESTS_BONUSES_TOKEN_BODY))
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self.__getTokenImages(complexToken.styleID), label=formatCountLabel(token.count), userName=self._getUserName(complexToken.styleID), labelFormatter=self._getLabelFormatter(bonus), tooltip=tooltip, align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus)))

        return result

    def _getUserName(self, styleID):
        webCache = self.eventsCache.prefetcher
        return i18n.makeString(webCache.getTokenInfo(styleID))

    def __getTokenImages(self, styleID):
        result = {}
        webCache = self.eventsCache.prefetcher
        for awardSizeKey, awardSizeVlaue in AWARDS_SIZES.getIterator():
            for tokenSizeKey, tokenSizeValue in TOKEN_SIZES.getIterator():
                if awardSizeKey == tokenSizeKey:
                    result[awardSizeVlaue] = webCache.getTokenImage(styleID, tokenSizeValue)

        return result


class CustomizationUnlockFormatter(TokenBonusFormatter):
    c11n = dependency.descriptor(ICustomizationService)
    __TOKEN_POSTFIX = ':camouflage'
    __ICON_NAME = 'camouflage'

    def _format(self, bonus):
        tokens = bonus.getTokens()
        unlockTokenID = findFirst(lambda ID: ID.endswith(self.__TOKEN_POSTFIX), tokens.keys())
        if unlockTokenID is not None:
            camouflages = self.c11n.getCamouflages(criteria=REQ_CRITERIA.CUSTOMIZATION.UNLOCKED_BY(unlockTokenID))
            images = {size:RES_ICONS.getBonusIcon(size, self.__ICON_NAME) for size in AWARDS_SIZES.ALL()}
            result = [PreformattedBonus(bonusName=bonus.getName(), label=formatCountLabel(len(camouflages)), align=LABEL_ALIGN.RIGHT, images=images, isSpecial=False, tooltip=makeTooltip(TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_HEADER, TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_BODY))]
        else:
            result = []
        return result


class VehiclesBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for vehicle, vehInfo in bonus.getVehicles():
            compensation = bonus.compensation(vehicle)
            if compensation:
                formatter = SimpleBonusFormatter()
                for bonusComp in compensation:
                    result.extend(formatter.format(bonusComp))

            else:
                tmanRoleLevel = bonus.getTmanRoleLevel(vehInfo)
                rentDays = bonus.getRentDays(vehInfo)
                rentBattles = bonus.getRentBattles(vehInfo)
                rentWins = bonus.getRentWins(vehInfo)
                if rentDays:
                    rentExpiryTime = time_utils.getCurrentTimestamp()
                    rentExpiryTime += rentDays * time_utils.ONE_DAY
                else:
                    rentExpiryTime = 0
                isRent = rentDays or rentBattles or rentWins
                result.append(PreformattedBonus(bonusName=bonus.getName(), label=self._getLabel(vehicle), userName=self._getUserName(vehicle), images=self._getImages(vehicle, isRent), isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.AWARD_VEHICLE, specialArgs=[vehicle.intCD,
                 tmanRoleLevel,
                 rentExpiryTime,
                 rentBattles,
                 rentWins], isCompensation=self._isCompensation(bonus)))

        return result

    def _getUserName(self, vehicle):
        return vehicle.userName

    @classmethod
    def _getLabel(cls, vehicle):
        if cls.__hasUniqueIcon(vehicle):
            return vehicle.userName
        return ''

    @classmethod
    def _getImages(cls, vehicle, isRent = False):
        result = {}
        for size in AWARDS_SIZES.ALL():
            image = '../maps/icons/quests/bonuses/{}/{}'.format(size, getItemIconName(vehicle.name))
            if image in RES_ICONS.MAPS_ICONS_QUESTS_BONUSES_ALL_ENUM:
                result[size] = image
            else:
                if isRent:
                    image = RES_ICONS.getRentVehicleAwardIcon(size)
                else:
                    image = RES_ICONS.getVehicleAwardIcon(size)
                result[size] = image

        return result

    @classmethod
    def __hasUniqueIcon(cls, vehicle):
        for size in AWARDS_SIZES.ALL():
            if cls._getImages(vehicle).get(size) != RES_ICONS.getVehicleAwardIcon(size):
                return True

        return False


class DossierBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for achievement in bonus.getAchievements():
            result.append(PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(achievement), images=self._getImages(achievement), isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.BATTLE_STATS_ACHIEVS, specialArgs=[achievement.getBlock(), achievement.getName(), achievement.getValue()], isCompensation=self._isCompensation(bonus)))

        for badge in bonus.getBadges():
            result.append(PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(badge), images=self._getImages(badge), isSpecial=True, specialAlias=self._getBadgeTooltipAlias(), specialArgs=[badge.badgeID], isCompensation=self._isCompensation(bonus)))

        return result

    @classmethod
    def _getUserName(cls, achievement):
        return achievement.getUserName()

    @classmethod
    def _getImages(cls, bonus):
        return {AWARDS_SIZES.SMALL: bonus.getSmallIcon(),
         AWARDS_SIZES.BIG: bonus.getBigIcon()}

    @classmethod
    def _getBadgeTooltipAlias(cls):
        return TOOLTIPS_CONSTANTS.BADGE


class EventBoardsDossierBonusFormatter(DossierBonusFormatter):

    @classmethod
    def _getBadgeTooltipAlias(cls):
        return TOOLTIPS_CONSTANTS.EVENT_BOARDS_BADGE


class BadgesGroupBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        badges = bonus.getBadges()
        groupID = bonus.getValue()
        result.append(PreformattedBonus(images={AWARDS_SIZES.SMALL: RES_ICONS.getEventBoardBadgesGroup(groupID)}, isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.EVENT_BOARDS_BADGES_GROUP, specialArgs=self.__badgesTooltipData(badges), isCompensation=self._isCompensation(bonus)))
        return result

    @classmethod
    def __badgesTooltipData(cls, badges):
        result = []
        for badge in badges:
            result.append({'name': badge.getUserName(),
             'imgSource': badge.getSmallIcon(),
             'desc': badge.getUserDescription()})

        return result


class TankmenBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for group in bonus.getTankmenGroups().itervalues():
            if group['skills']:
                key = 'with_skills'
            else:
                key = 'no_skills'
            label = '#quests:bonuses/item/tankmen/%s' % key
            result.append(PreformattedBonus(bonusName=bonus.getName(), userName=self._getUserName(key), images=self._getImages(bonus), tooltip=makeTooltip(TOOLTIPS.getAwardHeader(bonus.getName()), i18n.makeString(label, **group)), isCompensation=self._isCompensation(bonus)))

        return result

    @classmethod
    def _getUserName(cls, key):
        return i18n.makeString('#quests:bonusName/tankmen/%s' % key)

    @classmethod
    def _getImages(cls, bonus):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, bonus.getName())

        return result


class TankwomanBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for tmanInfo in bonus.getTankmenData():
            if tmanInfo.isFemale:
                bonusID = 'tankwoman'
                username = i18n.makeString(QUESTS.BONUSES_ITEM_TANKWOMAN)
                result.append(PreformattedBonus(bonusName=bonus.getName(), userName=username, images=self._getImages(bonusID), isSpecial=True, specialAlias=TOOLTIPS_CONSTANTS.PERSONAL_MISSIONS_TANKWOMAN, specialArgs=[]))
            else:
                bonusID = 'tankman'
                username = i18n.makeString(QUESTS.BONUSES_TANKMEN_DESCRIPTION, value=getRoleUserName(tmanInfo.role))
                result.append(PreformattedBonus(bonusName=bonus.getName(), userName=username, images=self._getImages(bonusID), tooltip=makeTooltip(i18n.makeString(QUESTS.BONUSES_TANKMEN_DESCRIPTION, value=getRoleUserName(tmanInfo.role)))))

        return result

    @classmethod
    def _getImages(cls, imageID):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, imageID)

        return result


class CustomizationsBonusFormatter(SimpleBonusFormatter):
    c11n = dependency.descriptor(ICustomizationService)

    def _format(self, bonus):
        result = []
        for item, data in zip(bonus.getCustomizations(), bonus.getList()):
            result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(item), userName=self._getUserName(item), isSpecial=True, label=formatCountLabel(item.get('value')), labelFormatter=self._getLabelFormatter(bonus), specialAlias=TOOLTIPS_CONSTANTS.TECH_CUSTOMIZATION_ITEM, specialArgs=[ data[o] for o in bonus.INFOTIP_ARGS_ORDER ], align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus)))

        return result

    @classmethod
    def _getImages(cls, item):
        result = {}
        c11nItem = cls.__getC11nItem(item)
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, c11nItem.itemTypeName)

        return result

    @classmethod
    def _getUserName(cls, item):
        c11nItem = cls.__getC11nItem(item)
        return i18n.makeString(QUESTS.getBonusName(c11nItem.itemTypeName))

    @classmethod
    def __getC11nItem(cls, item):
        itemTypeName = item.get('custType')
        itemID = item.get('id')
        itemTypeID = GUI_ITEM_TYPE_INDICES.get(itemTypeName)
        return cls.c11n.getItemByID(itemTypeID, itemID)


class OperationCustomizationsBonusFormatter(CustomizationsBonusFormatter):

    def _format(self, bonus):
        customizations = {}
        for item in bonus.getCustomizations():
            cType = item.get('custType')
            if cType in customizations:
                item, count = customizations[cType]
                customizations[cType] = (item, count + 1)
            else:
                customizations[cType] = (item, 1)

        result = []
        for item, count in customizations.itervalues():
            result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(item), userName=self._getUserName(item), label=formatCountLabel(count), labelFormatter=self._getLabelFormatter(bonus), align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus), isSpecial=False, tooltip=makeTooltip(TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_HEADER, TOOLTIPS.PERSONALMISSIONS_AWARDS_CAMOUFLAGE_BODY)))

        return result


class GoodiesBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for booster, count in bonus.getBoosters().iteritems():
            if booster is not None:
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(booster), isSpecial=True, label=formatCountLabel(count), labelFormatter=self._getLabelFormatter(bonus), userName=self._getUserName(booster), specialAlias=TOOLTIPS_CONSTANTS.BOOSTERS_BOOSTER_INFO, specialArgs=[booster.boosterID], align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus)))

        return result

    @classmethod
    def _getImages(cls, booster):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, booster.boosterGuiType)

        return result

    @classmethod
    def _getUserName(cls, booster):
        return booster.fullUserName


class ItemsBonusFormatter(SimpleBonusFormatter):

    def _format(self, bonus):
        result = []
        for item, count in bonus.getItems().iteritems():
            if item is not None and count:
                if item.itemTypeID == GUI_ITEM_TYPE.EQUIPMENT and 'avatar' in item.tags:
                    alias = TOOLTIPS_CONSTANTS.BATTLE_CONSUMABLE
                elif item.itemTypeID == GUI_ITEM_TYPE.SHELL:
                    alias = TOOLTIPS_CONSTANTS.AWARD_SHELL
                else:
                    alias = TOOLTIPS_CONSTANTS.AWARD_MODULE
                highlightType = None
                overlayType = None
                if item.itemTypeName == 'optionalDevice' and item.isDeluxe():
                    highlightType = SLOT_HIGHLIGHT_TYPES.NO_HIGHLIGHT
                    overlayType = SLOT_HIGHLIGHT_TYPES.EQUIPMENT_PLUS
                result.append(PreformattedBonus(bonusName=bonus.getName(), images=self._getImages(item), isSpecial=True, label=formatCountLabel(count), labelFormatter=self._getLabelFormatter(bonus), userName=self._getUserName(item), specialAlias=alias, specialArgs=[item.intCD], align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus), highlightType=highlightType, overlayType=overlayType))

        return result

    @classmethod
    def _getUserName(cls, item):
        return item.userName

    @classmethod
    def _getImages(cls, item):
        result = {}
        for size in AWARDS_SIZES.ALL():
            result[size] = RES_ICONS.getBonusIcon(size, item.getGUIEmblemID())

        return result


class Ny18ToysFormatter(SimpleBonusFormatter):
    _newYearController = dependency.descriptor(INewYearController)

    class XMassPreformattedBonus(PreformattedBonus):

        def __init__(self, *args, **kwargs):
            super(Ny18ToysFormatter.XMassPreformattedBonus, self).__init__(*args, **kwargs)
            self.level = None
            self.rank = None
            self.setting = None
            return

    def _format(self, bonus):
        outcome = []
        for bId in bonus.getValue():
            preformatted = self.XMassPreformattedBonus(bonusName=bonus.getName(), label=self._getLabel(bonus), userName=self._getUserName(bonus), labelFormatter=self._getLabelFormatter(bonus), images=self._getImages(bId), tooltip=bonus.getTooltip(), align=self._getLabelAlign(bonus), isCompensation=self._isCompensation(bonus), specialAlias=TOOLTIPS_CONSTANTS.NY_DECORATION, specialArgs=[bId], isSpecial=True)
            toyDesct = self._newYearController.toysDescrs.get(bId)
            level = 1
            rank = ''
            setting = ''
            if toyDesct:
                level = toyDesct.rank
                rank = 'rank{}'.format(toyDesct.rank)
                setting = '../maps/icons/ny/setting/setting_{}.png'.format(toyDesct.setting)
            else:
                LOG_WARNING("Couldn't find toy descriptor by provided bonusID '{}'. Rank and setting are skipped".format(bId))
            preformatted.level = level
            preformatted.rank = rank
            preformatted.setting = setting
            outcome.append(preformatted)

        return outcome

    def _getImages(self, bonusId):
        result = {}
        toyDesct = self._newYearController.toysDescrs.get(bonusId)
        if toyDesct:
            result[AWARDS_SIZES.SMALL] = toyDesct.slotIcon
            result[AWARDS_SIZES.BIG] = toyDesct.icon
        else:
            LOG_WARNING("Couldn't find toy descriptor by provided bonusID '{}'".format(bonusId))
        return result


class NY18DiscountFormatter(SimpleBonusFormatter):
    _newYearController = dependency.descriptor(INewYearController)

    def _format(self, bonus):
        outcome = []
        for bId in bonus.getValue():
            if bId in self._newYearController.vehDiscountsStorage.getDescriptors():
                outcome.append(self.__getVehiclePreformatted(bId))
            elif bId in self._newYearController.tankmanDiscountsStorage.getDescriptors():
                outcome.append(self.__getTankmenPreformatted())
            else:
                LOG_WARNING("Displaying of '{}' NY bonus has been skipped".format(bId))

        return outcome

    def __getVehiclePreformatted(self, bId):
        intLevel = self._newYearController.vehDiscountsStorage.extractLevelFromDiscountID(bId)
        vehLvlStr = makeString(TOOLTIPS.level(intLevel))
        discount = self._newYearController.vehDiscountsStorage.extractDiscountValueByLevel(intLevel)
        return PreformattedBonus(label=makeString(NY.DISCOUNT_FORMAT, discount=discount), labelFormatter=text_styles.stats, images={AWARDS_SIZES.BIG: RES_ICONS.MAPS_ICONS_NY_BONUSES_BIG_UNKNOWN_TANK,
         AWARDS_SIZES.SMALL: ''}, tooltip=makeTooltip(makeString(NY.REWARDSSCREEN_TOOLTIP_VEHICLE_HEADER, level=vehLvlStr), makeString(NY.REWARDSSCREEN_TOOLTIP_VEHICLE_BODY, discount=discount, level=vehLvlStr)), align=LABEL_ALIGN.RIGHT, isCompensation=False, isSpecial=False)

    def __getTankmenPreformatted(self):
        return PreformattedBonus(images={AWARDS_SIZES.BIG: RES_ICONS.MAPS_ICONS_NY_BONUSES_BIG_TANK_WOMEN,
         AWARDS_SIZES.SMALL: ''}, isCompensation=False, specialAlias=TOOLTIPS_CONSTANTS.PERSONAL_MISSIONS_NY_TANKWOMAN, isSpecial=True)


class NY18BoxFormatter(TokenBonusFormatter):
    _newYearController = dependency.descriptor(INewYearController)

    def _format(self, bonus):
        preformatted = super(NY18BoxFormatter, self)._format(bonus)
        for tokenID, token in bonus.getTokens().iteritems():
            if tokenID in self._newYearController.boxStorage.getDescriptors():
                preformatted.append(PreformattedBonus(bonusName=bonus.getName(), images={AWARDS_SIZES.BIG: RES_ICONS.MAPS_ICONS_NY_BONUSES_BIG_BOX,
                 AWARDS_SIZES.SMALL: RES_ICONS.MAPS_ICONS_NY_BONUSES_SMALL_BOX}, label=formatCountLabel(token.count), labelFormatter=self._getLabelFormatter(bonus), tooltip=makeTooltip(makeString(NY.HANGAR_BONUSINFO_TOOLTIP_HEADER), makeString(NY.HANGAR_BONUSINFO_TOOLTIP_BODY)), align=LABEL_ALIGN.RIGHT, isCompensation=self._isCompensation(bonus)))

        return preformatted