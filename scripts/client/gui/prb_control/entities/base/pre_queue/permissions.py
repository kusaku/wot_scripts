# Embedded file name: scripts/client/gui/prb_control/entities/base/pre_queue/permissions.py
from gui.prb_control.entities.base.permissions import IPrbPermissions

class PreQueuePermissions(IPrbPermissions):
    """
    Persmissions class for prequeue actions.
    """

    def __init__(self, isInQueue):
        super(PreQueuePermissions, self).__init__()
        self.__isInQueue = isInQueue

    def canChangeVehicle(self):
        return not self.__isInQueue

    def canCreateSquad(self):
        return not self.__isInQueue