# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/rankedBattles/RankedBattlesBattleResults.py
from account_helpers import AccountSettings
from account_helpers.AccountSettings import ENABLE_RANKED_ANIMATIONS
from gui.Scaleform.daapi.view.meta.RankedBattlesBattleResultsMeta import RankedBattlesBattleResultsMeta
from gui.Scaleform.genConsts.RANKEDBATTLES_ALIASES import RANKEDBATTLES_ALIASES
from helpers import dependency
from skeletons.gui.game_control import IRankedBattlesController

class RankedBattlesBattleResults(RankedBattlesBattleResultsMeta):
    rankedController = dependency.descriptor(IRankedBattlesController)

    def __init__(self, ctx = None):
        super(RankedBattlesBattleResults, self).__init__()
        raise 'rankedResultsVO' in ctx or AssertionError
        self.__rankedResultsVO = ctx['rankedResultsVO']
        raise 'vehicle' in ctx or AssertionError
        self.__vehicle = ctx['vehicle']
        if not 'rankInfo' in ctx:
            raise AssertionError
            self.__rankInfo = ctx['rankInfo']
            self.__questsProgress = ctx['questsProgress']
            accProgress = (self.__rankInfo.accRank, self.__rankInfo.accStep)
            vehProgress = (self.__rankInfo.vehRank, self.__rankInfo.vehStep)
            prevAccProgress = (self.__rankInfo.prevAccRank, self.__rankInfo.prevAccStep)
            prevVehProgress = (self.__rankInfo.prevVehRank, self.__rankInfo.prevVehStep)
            maxProgress = max(accProgress, prevAccProgress)
            self.__ranks = self.rankedController.buildRanksChain(accProgress, maxProgress, prevAccProgress)
            accRanksCount = self.rankedController.getAccRanksTotal()
            if self.__rankInfo.accRank <= accRanksCount and self.__rankInfo.vehRank < 1:
                maxVehProgress = self.__rankInfo.accRank == accRanksCount and max(vehProgress, prevVehProgress)
                vehRanks = self.rankedController.buildVehicleRanksChain(vehProgress, maxVehProgress, prevVehProgress, self.__vehicle)
                self.__ranks.extend(vehRanks)
            self.__setRanks(accProgress, prevAccProgress)
        else:
            maxVehProgress = max(vehProgress, prevVehProgress)
            vehRanks = self.rankedController.buildVehicleRanksChain(vehProgress, maxVehProgress, prevVehProgress, self.__vehicle)
            self.__ranks.extend(vehRanks)
            self.__setRanks(vehProgress, prevVehProgress, accRanksCount)

    def onEscapePress(self):
        self.__close()

    def onWindowClose(self):
        self.__close()

    def closeView(self):
        self.__close()

    def animationCheckBoxSelected(self, value):
        AccountSettings.setSettings(ENABLE_RANKED_ANIMATIONS, value)

    @property
    def rankedWidget(self):
        """
        This is big widget in the middle of view
        :return: instance of the component. It is related only to this view
        """
        return self.getComponent(RANKEDBATTLES_ALIASES.RANKED_BATTLE_RESULTS_WIDGET)

    def _populate(self):
        super(RankedBattlesBattleResults, self)._populate()
        self.__updateRankedWidget()
        self.as_setDataS(self.__rankedResultsVO)

    def __setRanks(self, progress, prevProgress, adjustment = 0):
        rankID, _ = progress
        lastRankID, _ = prevProgress
        rankID += adjustment
        lastRankID += adjustment
        self.__currentRank = self.__ranks[rankID]
        self.__lastRank = self.__ranks[lastRankID]

    def __updateRankedWidget(self):
        if self.rankedWidget is not None:
            self.rankedWidget.update(self.__ranks, self.__currentRank, self.__lastRank)
        return

    def __close(self):
        if self.rankedController.awardWindowShouldBeShown(self.__rankInfo):
            self.rankedController.showRankedAwardWindow(self.__rankInfo, self.__vehicle, self.__questsProgress)
        self.destroy()