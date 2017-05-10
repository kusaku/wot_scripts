# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/rankedBattles/RankedBattlesSeasonCompleteView.py
import BigWorld
from adisp import process
from gui.Scaleform.daapi.view.lobby.rankedBattles.finish_awards_view import FinishAwardsView
from gui.Scaleform.daapi.view.meta.RankedBattlesSeasonCompleteViewMeta import RankedBattlesSeasonCompleteViewMeta
from gui.Scaleform.locale.RANKED_BATTLES import RANKED_BATTLES
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.ranked_battles import ranked_helpers
from gui.shared.money import Currency
from shared_utils import first

class RankedBattlesSeasonCompleteView(RankedBattlesSeasonCompleteViewMeta, FinishAwardsView):

    def __init__(self, ctx = None):
        super(RankedBattlesSeasonCompleteView, self).__init__(ctx)
        FinishAwardsView.__init__(self, ctx)

    def closeView(self):
        self.__close()

    def onSoundTrigger(self, triggerName):
        self._playSound(triggerName)

    def showRating(self):
        self.rankedController.openWebLeaguePage()
        self.__close()

    def _populate(self):
        super(RankedBattlesSeasonCompleteView, self)._populate()
        self.__setData()

    @process
    def __setData(self):
        seasonID, cohort, _ = ranked_helpers.getRankedDataFromTokenQuestID(self._quest.getID())
        season = self.rankedController.getSeason(int(seasonID))
        if season is not None:
            leagueData = yield self.rankedController.getLeagueData()
            if leagueData is not None:
                position = BigWorld.wg_getNiceNumberFormat(leagueData['position'])
            else:
                position = 'N/A'
            crystalsBonus = first(self._quest.getBonuses(Currency.CRYSTAL))
            if crystalsBonus is not None:
                crystalsCount = crystalsBonus.getValue()
            else:
                crystalsCount = 0
            self.as_setDataS({'boxImage': RES_ICONS.getRankedBoxIcon('450x400', 'metal', '_opened', cohort),
             'scoresValue': BigWorld.wg_getNiceNumberFormat(season.getPoints()),
             'scoresLabel': RANKED_BATTLES.SEASONCOMPLETE_TOTALSCORES,
             'placeValue': position,
             'placeHolderVisible': True,
             'placeLabel': RANKED_BATTLES.SEASONCOMPLETE_PLACEINRATING,
             'currencyLabel': RANKED_BATTLES.SEASONCOMPLETE_PROXYCURRENCYLABEL,
             'currencyValue': str(crystalsCount),
             'congratulationTitle': RANKED_BATTLES.SEASONCOMPLETE_SEASONRESULTS,
             'nextButtonLabel': RANKED_BATTLES.AWARDS_YES,
             'awards': self._packAwards()})
        return

    def _boxAnimationData(self):
        _, cohortNumber, _ = ranked_helpers.getRankedDataFromTokenQuestID(self._quest.getID())
        return ('metal', cohortNumber)

    def __close(self):
        self.destroy()
        self._closeCallback()