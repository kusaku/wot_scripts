# Embedded file name: scripts/client/gui/Scaleform/daapi/view/bootcamp/BCPersonalCase.py
from gui.Scaleform.daapi.view.meta.BCPersonalCaseMeta import BCPersonalCaseMeta
from gui.Scaleform.daapi.view.lobby.PersonalCase import PersonalCaseDataProvider
from adisp import async
from helpers import dependency
from skeletons.gui.shared import IItemsCache
from debug_utils import LOG_DEBUG
from skeletons.gui.game_control import IBootcampController
from bootcamp.Bootcamp import g_bootcamp
from bootcamp.BootcampGarage import g_bootcampGarage

class BCPersonalCaseDataProvider(PersonalCaseDataProvider):

    def __init__(self, tmanInvID):
        super(BCPersonalCaseDataProvider, self).__init__(tmanInvID)

    @async
    def getSkillsData(self, callback):
        itemsCache = dependency.instance(IItemsCache)
        tankman = itemsCache.items.getTankman(self.tmanInvID)
        data = tankman.getSkillsToLearn()
        skillSixthSense = None
        skillComouflage = None
        for skills in data:
            for skill in skills['skills']:
                if skill['id'] == 'commander_sixthSense':
                    skillSixthSense = skill
                elif skill['id'] == 'camouflage':
                    skillComouflage = skill
                else:
                    skill['enabled'] = False

        skillsGroupsRemove = list()
        for skills in data:
            if skills['id'] == 'common':
                if skillComouflage is not None:
                    skills['skills'].remove(skillComouflage)
                    skills['skills'].insert(0, skillComouflage)
                if skillSixthSense is not None:
                    skillComouflage['enabled'] = False
                    skills['skills'].insert(0, skillSixthSense)
                scrollCountSkills = g_bootcamp.getContextIntParameter('scrollCountSkills')
                if len(skills['skills']) > scrollCountSkills:
                    del skills['skills'][scrollCountSkills:]
            else:
                skillsGroupsRemove.append(skills)

        for skills in skillsGroupsRemove:
            data.remove(skills)

        callback(data)
        return


class BCPersonalCase(BCPersonalCaseMeta):

    def __init__(self, ctx = None):
        LOG_DEBUG('BCPersonalCase.__init__')
        super(BCPersonalCase, self).__init__(ctx)
        self.dataProvider = BCPersonalCaseDataProvider(self.tmanInvID)
        self.__skillSelected = False
        self.__skillAdded = False
        itemsCache = dependency.instance(IItemsCache)
        self.__tman = itemsCache.items.getTankmanDossier(self.tmanInvID)

    def _populate(self):
        LOG_DEBUG('BCPersonalCase._populate')
        super(BCPersonalCase, self)._populate()
        if self.checkRole():
            g_bootcampGarage.runViewAlias('bootcampPresonalCase')

    def _dispose(self):
        super(BCPersonalCase, self)._dispose()
        g_bootcampGarage.runViewAlias('hangar')

    def checkRole(self):
        return self.__tman.tmanDescr.role == 'commander'

    def onSkillClick(self, skillId):
        if self.checkRole() and not self.__skillSelected and skillId == 'commander_sixthSense':
            self.__skillSelected = True
            g_bootcampGarage.hidePrevShowNextHint()

    def addTankmanSkill(self, invengoryID, skillName):
        super(BCPersonalCase, self).addTankmanSkill(invengoryID, skillName)
        if self.checkRole() and skillName == 'commander_sixthSense':
            self.__skillAdded = True
            g_bootcampGarage.hideAllHints()
            g_bootcampGarage.runCustomAction('msgSkillsPerks')

    def onWindowClose(self):
        super(BCPersonalCase, self).onWindowClose()