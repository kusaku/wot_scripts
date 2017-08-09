# Embedded file name: scripts/client/bootcamp/scenery/missions/mission_4.py
from bootcamp.scenery.AbstractMission import AbstractMission

class Mission4(AbstractMission):

    def __init__(self, assistant):
        super(Mission4, self).__init__(assistant)

    def destroy(self):
        super(Mission4, self).destroy()

    def start(self):
        super(Mission4, self).start()
        self.playSound2D('vo_bc_main_task')
        self.playSound2D('bc_main_tips_task_start')
        self._avatar.muteSounds(('crew_member_contusion', 'track_destroyed', 'fire_started', 'gunner_killed'))

    def update(self):
        super(Mission4, self).update()

    def onPlayerDetectEnemy(self, new, lost):
        self._playCombatMusic()

    def stop(self):
        self._avatar.muteSounds(())