# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/rankedBattles/RankedBattlesWelcomeView.py
from account_helpers import AccountSettings
from account_helpers.AccountSettings import GUI_START_BEHAVIOR
from gui.Scaleform.daapi import LobbySubView
from gui.Scaleform.daapi.settings.views import VIEW_ALIAS
from gui.Scaleform.daapi.view.meta.RankedBattlesWelcomeViewMeta import RankedBattlesWelcomeViewMeta
from gui.Scaleform.locale.RANKED_BATTLES import RANKED_BATTLES
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.shared import events, EVENT_BUS_SCOPE
from gui.shared.formatters import text_styles
from gui.shared.utils.functions import makeTooltip
from helpers import dependency
from skeletons.account_helpers.settings_core import ISettingsCore

class RankedBattlesWelcomeView(LobbySubView, RankedBattlesWelcomeViewMeta):
    settingsCore = dependency.descriptor(ISettingsCore)
    __background_alpha__ = 0.5

    def __init__(self, ctx = None):
        super(RankedBattlesWelcomeView, self).__init__()

    def onEscapePress(self):
        self.__close()

    def onCloseBtnClick(self):
        self.onAnimationFinished()
        self.__close()

    def onNextBtnClick(self):
        self.__close()

    def onAnimationFinished(self):
        self.soundManager.stopAllSounds()
        filters = self.__getFilters()
        filters['isRankedWelcomeViewShowed'] = True
        self.__setFilters(filters)

    def onSoundTrigger(self, eventName):
        self.soundManager.playSound(eventName)

    def _populate(self):
        super(RankedBattlesWelcomeView, self)._populate()
        self.as_setDataS(self.__getData())

    def __getData(self):
        filters = self.__getFilters()
        isCompleted = filters['isRankedWelcomeViewStarted']
        filters['isRankedWelcomeViewStarted'] = True
        self.__setFilters(filters)
        positiveTeamStr = text_styles.bonusAppliedText(RANKED_BATTLES.WELCOMESCREEN_POSITIVE_TEAM)
        negativeTeamStr = text_styles.error(RANKED_BATTLES.WELCOMESCREEN_NEGATIVE_TEAM)
        ranks = [ RES_ICONS.getRankIcon('114x160', i) for i in xrange(1, 6) ]
        ranks.append(RES_ICONS.MAPS_ICONS_RANKEDBATTLES_RANKS_114X160_RANKVEHMASTER)
        return {'header': text_styles.superPromoTitle(RANKED_BATTLES.WELCOMESCREEN_HEADER),
         'rules': [{'image': RES_ICONS.MAPS_ICONS_RANKEDBATTLES_RANKEDBATTESVIEW_ICN_TANKS,
                    'description': text_styles.hightlight(RANKED_BATTLES.WELCOMESCREEN_LEFTRULE),
                    'tooltip': makeTooltip(RANKED_BATTLES.WELCOMESCREEN_LEFTRULETOOLTIP_HEADER, RANKED_BATTLES.WELCOMESCREEN_LEFTRULETOOLTIP_BODY)}, {'image': RES_ICONS.MAPS_ICONS_RANKEDBATTLES_RANKEDBATTESVIEW_ICN_CREW,
                    'description': text_styles.hightlight(RANKED_BATTLES.WELCOMESCREEN_CENTERRULE),
                    'tooltip': makeTooltip(RANKED_BATTLES.WELCOMESCREEN_CENTERRULETOOLTIP_HEADER, RANKED_BATTLES.WELCOMESCREEN_CENTERRULETOOLTIP_BODY)}, {'image': RES_ICONS.MAPS_ICONS_RANKEDBATTLES_RANKEDBATTESVIEW_AWARD,
                    'description': text_styles.hightlight(RANKED_BATTLES.WELCOMESCREEN_RIGHTRULE),
                    'tooltip': makeTooltip(RANKED_BATTLES.WELCOMESCREEN_RIGHTRULETOOLTIP_HEADER, RANKED_BATTLES.WELCOMESCREEN_RIGHTRULETOOLTIP_BODY)}],
         'ranks': ranks,
         'rulePositive': {'image': RES_ICONS.MAPS_ICONS_RANKEDBATTLES_RANKEDBATTESVIEW_ICON_TOP12_106X98,
                          'description': text_styles.hightlight(RANKED_BATTLES.WELCOMESCREEN_POSITIVE_BODY) % {'team': positiveTeamStr}},
         'ruleNegative': {'image': RES_ICONS.MAPS_ICONS_RANKEDBATTLES_RANKEDBATTESVIEW_ICON_TOP3_106X98,
                          'description': text_styles.hightlight(RANKED_BATTLES.WELCOMESCREEN_NEGATIVE_BODY) % {'team': negativeTeamStr}},
         'ranksDescription': text_styles.promoSubTitle(RANKED_BATTLES.WELCOMESCREEN_RANKSDESCR),
         'equalityText': RANKED_BATTLES.WELCOMESCREEN_EQUALITYTEXT,
         'rulesDelimeterText': text_styles.promoSubTitle(RANKED_BATTLES.WELCOMESCREEN_RULESDELIMETER),
         'btnLbl': RANKED_BATTLES.WELCOMESCREEN_BTN,
         'btnTooltip': makeTooltip(RANKED_BATTLES.RANKEDBATTLEVIEW_NOTRANKEDBLOCK_OKTOOLTIP_HEADER, RANKED_BATTLES.RANKEDBATTLEVIEW_NOTRANKEDBLOCK_OKTOOLTIP_BODY),
         'closeLbl': RANKED_BATTLES.WELCOMESCREEN_CLOSEBTN,
         'closeBtnTooltip': makeTooltip(RANKED_BATTLES.WELCOMESCREEN_CLOSEBTNTOOLTIP_HEADER, RANKED_BATTLES.WELCOMESCREEN_CLOSEBTNTOOLTIP_BODY),
         'bgImage': RES_ICONS.MAPS_ICONS_RANKEDBATTLES_BG_RANK_BLUR,
         'isComplete': bool(isCompleted)}

    def __close(self):
        self.fireEvent(events.LoadViewEvent(VIEW_ALIAS.LOBBY_HANGAR), scope=EVENT_BUS_SCOPE.LOBBY)
        self.destroy()

    def __getFilters(self):
        defaults = AccountSettings.getFilterDefault(GUI_START_BEHAVIOR)
        return self.settingsCore.serverSettings.getSection(GUI_START_BEHAVIOR, defaults)

    def __setFilters(self, filters):
        self.settingsCore.serverSettings.setSectionSettings(GUI_START_BEHAVIOR, filters)