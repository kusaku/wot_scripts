# Embedded file name: scripts/client/gui/shared/gui_items/badge.py
from account_helpers import AccountSettings
from account_helpers.AccountSettings import LAST_BADGES_VISIT
from dossiers2.ui.achievements import BADGES_BLOCK
from gui.Scaleform.locale.BADGE import BADGE
from gui.Scaleform.settings import getBadgeIconPath, getBadgeHighlightIconPath, BADGES_ICONS, BADGES_HIGHLIGHTS
from gui.shared.gui_items.gui_item import GUIItem
from helpers import i18n
from shared_utils import CONST_CONTAINER

class BADGE_TYPES(CONST_CONTAINER):
    OBSOLETE = 1
    COLLAPSIBLE = 2


class Badge(GUIItem):
    """
    Badge gui item object, that stores server date and defines whether it is selected, achieved and etc.
    Also has all necessary gui methods for representation in GUI.
    """
    __slots__ = ('badgeID', 'data', 'isSelected', 'isAchieved', 'achievedAt', 'group')

    def __init__(self, data, proxy = None):
        super(Badge, self).__init__(proxy)
        self.badgeID = data['id']
        self.data = data
        self.group = data.get('group')
        self.isSelected = False
        self.isAchieved = False
        self.achievedAt = None
        if proxy is not None and proxy.dossiers.isSynced() and proxy.badges.isSynced():
            self.isSelected = self.badgeID in proxy.badges.selected
            receivedBadges = proxy.getAccountDossier().getDossierDescr()[BADGES_BLOCK]
            self.isAchieved = self.badgeID in receivedBadges
            if self.isAchieved:
                self.achievedAt = receivedBadges[self.badgeID]
        return

    def __cmp__(self, other):
        """
        Standard comparision method that compares two badges by:
        - is it achieved
        - if both - by achievement date (latest first)
        - otherwise by weight
        """
        if self.achievedAt == other.achievedAt:
            return cmp(self.getWeight(), other.getWeight())
        elif self.achievedAt is None:
            return 1
        elif other.achievedAt is None:
            return -1
        else:
            return cmp(other.achievedAt, self.achievedAt)

    def getBadgeClass(self):
        return self.data.get('class', 0)

    def getName(self):
        """
        Gets name of badge from it's data.
        Could be used to differ badges by type or smth.
        """
        return self.data['name']

    def getWeight(self):
        return self.data['weight']

    def isObsolete(self):
        return self.__checkType(BADGE_TYPES.OBSOLETE)

    def isCollapsible(self):
        return self.__checkType(BADGE_TYPES.COLLAPSIBLE)

    def getHugeIcon(self):
        return getBadgeIconPath(BADGES_ICONS.X220, self.badgeID)

    def getBigIcon(self):
        return getBadgeIconPath(BADGES_ICONS.X80, self.badgeID)

    def getSmallIcon(self):
        return getBadgeIconPath(BADGES_ICONS.X48, self.badgeID)

    def getThumbnailIcon(self):
        return getBadgeIconPath(BADGES_ICONS.X24, self.badgeID)

    def getUserName(self):
        key = BADGE.badgeName(self.badgeID)
        return i18n.makeString(key)

    def getShortUserName(self):
        key = BADGE.getShortName(self.badgeID)
        if key is None:
            return self.getUserName()
        else:
            return i18n.makeString(key)

    def getUserDescription(self):
        key = BADGE.badgeDescriptor(self.badgeID)
        return i18n.makeString(key)

    def getHighlightIcon(self):
        if self.getName().startswith('ranked'):
            return getBadgeHighlightIconPath(BADGES_HIGHLIGHTS.RED)
        if self.getName().startswith('personal_missions'):
            return getBadgeHighlightIconPath(BADGES_HIGHLIGHTS.VIOLET)
        if self.getName().startswith('event_boards'):
            return getBadgeHighlightIconPath(BADGES_HIGHLIGHTS.GREEN)
        if self.getName().startswith('global_map'):
            return getBadgeHighlightIconPath(BADGES_HIGHLIGHTS.GOLD)
        return ''

    def isNew(self):
        """
        Indicate that player is haven't see the badge yet
        :return: bool
        """
        result = False
        if self.isAchieved:
            lastBadgesVisit = AccountSettings.getSettings(LAST_BADGES_VISIT)
            if lastBadgesVisit is not None:
                result = lastBadgesVisit < self.achievedAt
            else:
                result = True
        return result

    def __checkType(self, badgeType):
        return self.data['type'] & badgeType > 0