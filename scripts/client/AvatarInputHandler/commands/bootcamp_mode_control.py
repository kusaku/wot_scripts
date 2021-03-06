# Embedded file name: scripts/client/AvatarInputHandler/commands/bootcamp_mode_control.py
import BigWorld
import constants
import Keys
from AvatarInputHandler.commands.input_handler_command import InputHandlerCommand

class BootcampModeControl(InputHandlerCommand):

    def handleKeyEvent(self, isDown, key, mods, event = None):
        playerBase = BigWorld.player().base
        if isDown and constants.HAS_DEV_RESOURCES:
            if key == Keys.KEY_F3:
                playerBase.setDevelopmentFeature('heal', 0, '')
                return True
            if key == Keys.KEY_F4:
                playerBase.setDevelopmentFeature('reload_gun', 0, '')
                return True
            if key == Keys.KEY_F5:
                playerBase.setDevelopmentFeature('teleportToShotPoint', 0, '')
                return True
            if key == Keys.KEY_P and BigWorld.isKeyDown(Keys.KEY_CAPSLOCK):
                playerBase.setDevelopmentFeature('kill_bots', 0, '')
                return True