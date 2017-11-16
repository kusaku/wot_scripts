# Embedded file name: scripts/client/gui/battle_control/controllers/game_messages_ctrl.py
import weakref
from PlayerEvents import g_playerEvents
from gui.battle_control.battle_constants import BATTLE_CTRL_ID
from gui.battle_control.view_components import IViewComponentsController
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

class GameMessagesController(IViewComponentsController):
    """
    Controller adds messages in UI.
    """
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self, setup):
        super(GameMessagesController, self).__init__()
        self.__arenaVisitor = weakref.proxy(setup.arenaVisitor)
        self.__ui = None
        return

    def getControllerID(self):
        """ Gets unique ID of controller.
        :return: integer.
        """
        return BATTLE_CTRL_ID.GAME_MESSAGES_PANEL

    def startControl(self):
        """Start to control states. It's just implementation of interface."""
        if self.__arenaVisitor.hasGameEndMessage():
            g_playerEvents.onRoundFinished += self.__onRoundFinished

    def setViewComponents(self, component):
        self.__ui = component

    def clearViewComponents(self):
        if self.__ui:
            self.__ui.destroy()
        self.__ui = None
        return

    def stopControl(self):
        """Stops to control states."""
        if self.__arenaVisitor.hasGameEndMessage():
            g_playerEvents.onRoundFinished -= self.__onRoundFinished
        self.__arenaVisitor = None
        return

    def __onRoundFinished(self, winningTeam, reason):
        if self.__ui:
            self.__ui.sendEndGameMessage(winningTeam, reason)


def createGameMessagesController(setup):
    return GameMessagesController(setup)