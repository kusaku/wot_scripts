# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/FalloutBattleSelectorWindow.py
from adisp import process
from constants import FALLOUT_BATTLE_TYPE, QUEUE_TYPE
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.game_control import getFalloutCtrl
from gui.prb_control.context import pre_queue_ctx
from gui.prb_control.prb_helpers import GlobalListener
from gui.shared import events, EVENT_BUS_SCOPE
from gui.Scaleform.daapi.view.meta.FalloutBattleSelectorWindowMeta import FalloutBattleSelectorWindowMeta
from gui.Scaleform.locale.FALLOUT import FALLOUT
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.shared.formatters.text_styles import promoSubTitle, main
from gui.shared.utils.functions import makeTooltip

class FalloutBattleSelectorWindow(FalloutBattleSelectorWindowMeta, GlobalListener):

    def __init__(self, ctx = None):
        super(FalloutBattleSelectorWindow, self).__init__(ctx)
        self.__falloutCtrl = None
        return

    def _populate(self):
        super(FalloutBattleSelectorWindow, self)._populate()
        self.addListener(events.HideWindowEvent.HIDE_BATTLE_SESSION_WINDOW, self.__handleFalloutWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)
        self.startGlobalListening()
        self.__falloutCtrl = getFalloutCtrl()
        self.__falloutCtrl.onSettingsChanged += self.__updateFalloutSettings
        self.as_setInitDataS({'windowTitle': FALLOUT.BATTLESELECTORWINDOW_TITLE,
         'headerTitleStr': promoSubTitle(FALLOUT.BATTLESELECTORWINDOW_HEADERTITLESTR),
         'headerDescStr': main(FALLOUT.BATTLESELECTORWINDOW_HEADERDESC),
         'dominationBattleTitleStr': promoSubTitle(FALLOUT.BATTLESELECTORWINDOW_DOMINATION_TITLE),
         'dominationBattleDescStr': main(FALLOUT.BATTLESELECTORWINDOW_DOMINATION_DESCR),
         'dominationBattleBtnStr': FALLOUT.BATTLESELECTORWINDOW_DOMINATIONBATTLEBTNLBL,
         'multiteamTitleStr': promoSubTitle(FALLOUT.BATTLESELECTORWINDOW_MULTITEAM_TITLE),
         'multiteamDescStr': main(FALLOUT.BATTLESELECTORWINDOW_MULTITEAM_DESCR),
         'multiteamBattleBtnStr': FALLOUT.BATTLESELECTORWINDOW_MULTITEAMBATTLEBTNLBL,
         'bgImg': RES_ICONS.MAPS_ICONS_LOBBY_FALLOUTBATTLESELECTORBG,
         'multiteamAutoSquadEnabled': self.__falloutCtrl.isAutomatch(),
         'multiteamAutoSquadLabel': FALLOUT.FALLOUTBATTLESELECTORWINDOW_AUTOSQUAD_LABEL,
         'multiteamAutoSquadInfoTooltip': makeTooltip(TOOLTIPS.FALLOUTBATTLESELECTORWINDOW_INFO_HEADER, TOOLTIPS.FALLOUTBATTLESELECTORWINDOW_INFO_BODY)})
        if self.prbDispatcher.getFunctionalState().hasLockedState or not self.__falloutCtrl.canChangeBattleType():
            self.as_setBtnStatesS(self.__getBtnsStateData(False))

    def onSelectCheckBoxAutoSquad(self, isSelected):
        self.__falloutCtrl.setAutomatch(isSelected)

    def _dispose(self):
        self.stopGlobalListening()
        self.removeListener(events.HideWindowEvent.HIDE_BATTLE_SESSION_WINDOW, self.__handleFalloutWindowHide, scope=EVENT_BUS_SCOPE.LOBBY)
        if self.__falloutCtrl:
            self.__falloutCtrl.onSettingsChanged -= self.__updateFalloutSettings
        self.__falloutCtrl = None
        super(FalloutBattleSelectorWindow, self)._dispose()
        return

    def onWindowMinimize(self):
        self.destroy()

    def onWindowClose(self):
        if self.prbDispatcher.getFunctionalState().hasLockedState:
            self.destroy()
        else:
            self.__leaveFallout()

    def onDominationBtnClick(self):
        self.__falloutCtrl.setBattleType(FALLOUT_BATTLE_TYPE.CLASSIC)
        self.onWindowMinimize()

    def onMultiteamBtnClick(self):
        self.__falloutCtrl.setBattleType(FALLOUT_BATTLE_TYPE.MULTITEAM)
        self.onWindowMinimize()

    def __getBtnsStateData(self, isEnabled):
        return {'dominationBtnEnabled': isEnabled,
         'multiteamBtnEnabled': isEnabled,
         'closeBtnEnabled': isEnabled,
         'autoSquadCheckboxEnabled': isEnabled}

    def onEnqueued(self, queueType, *args):
        self.as_setBtnStatesS(self.__getBtnsStateData(False))

    def onDequeued(self, queueType, *args):
        self.as_setBtnStatesS(self.__getBtnsStateData(True))

    def onUnitFlagsChanged(self, flags, timeLeft):
        if self.unitFunctional.hasLockedState():
            if flags.isInSearch() or flags.isInQueue() or flags.isInArena():
                self.as_setBtnStatesS(self.__getBtnsStateData(False))
        else:
            self.as_setBtnStatesS(self.__getBtnsStateData(True))

    def __handleFalloutWindowHide(self, _):
        self.destroy()

    def __updateFalloutSettings(self):
        if not self.__falloutCtrl.isEnabled():
            return self.onWindowClose()
        if self.prbDispatcher.getFunctionalState().hasLockedState or not self.__falloutCtrl.canChangeBattleType():
            self.as_setBtnStatesS(self.__getBtnsStateData(False))
        else:
            self.as_setBtnStatesS(self.__getBtnsStateData(True))

    @process
    def __leaveFallout(self):
        yield self.prbDispatcher.join(pre_queue_ctx.JoinModeCtx(QUEUE_TYPE.RANDOMS))