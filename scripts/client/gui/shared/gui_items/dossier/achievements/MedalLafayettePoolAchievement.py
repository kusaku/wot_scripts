# Embedded file name: scripts/client/gui/shared/gui_items/dossier/achievements/MedalLafayettePoolAchievement.py
from dossiers2.ui.achievements import ACHIEVEMENT_BLOCK as _AB
from abstract import RegularExtAchievement
from abstract.mixins import NoProgressBar
from arena_achievements import ACHIEVEMENT_CONDITIONS, ACHIEVEMENT_CONDITIONS_EXT

class MedalLafayettePoolAchievement(NoProgressBar, RegularExtAchievement):

    def __init__(self, dossier, value = None):
        RegularExtAchievement.__init__(self, 'medalLafayettePool', _AB.TOTAL, dossier, value)

    def _getStandardValues(self):
        return str(ACHIEVEMENT_CONDITIONS[self._getActualName()]['minKills']) + '-' + str(ACHIEVEMENT_CONDITIONS[self._getActualName()]['maxKills'])

    def _getExtValues(self):
        return str(ACHIEVEMENT_CONDITIONS_EXT[self._getActualName()]['minKills']) + '-' + str(ACHIEVEMENT_CONDITIONS_EXT[self._getActualName()]['maxKills'])