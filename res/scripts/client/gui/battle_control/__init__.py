# Embedded file name: scripts/client/gui/battle_control/__init__.py
from gui.battle_control.battle_session import BattleSessionProvider
from gui.battle_control.controllers import BattleSessionSetup
__all__ = ('BattleSessionSetup', 'g_sessionProvider')
g_sessionProvider = BattleSessionProvider()