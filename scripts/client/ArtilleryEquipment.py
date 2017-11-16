# Embedded file name: scripts/client/ArtilleryEquipment.py
from AvatarInputHandler import mathUtils
import BigWorld
from Math import Vector3

class ArtilleryEquipment(BigWorld.UserDataObject):
    launchVelocity = property(lambda self: self.__launchVelocity)

    def __init__(self):
        BigWorld.UserDataObject.__init__(self)
        launchDir = mathUtils.createRotationMatrix((self.__dict__['yaw'], self.__dict__['pitch'], 0)).applyToAxis(2)
        launchDir.normalise()
        self.__launchVelocity = launchDir * self.speed