# Embedded file name: scripts/client/gui/miniclient/lobby/strongholds/aspects.py
from helpers import aop
from gui.Scaleform.genConsts.FORTIFICATION_ALIASES import FORTIFICATION_ALIASES
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS

class MakeStrongholdsUnavailable(aop.Aspect):

    def atCall(self, cd):
        cd.avoid()
        tooltip = TOOLTIPS.HEADER_BUTTONS_FORTS_SANDBOX_TURNEDOFF
        return {'label': MENU.HEADERBUTTONS_FORTS,
         'value': FORTIFICATION_ALIASES.FORTIFICATIONS2_VIEW_ALIAS,
         'tooltip': tooltip,
         'enabled': False}