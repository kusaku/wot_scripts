# Embedded file name: scripts/client/gui/prb_control/entities/ranked/pre_queue/ctx.py
from constants import QUEUE_TYPE
from gui.prb_control.entities.base.pre_queue.ctx import QueueCtx
from gui.shared.utils.decorators import ReprInjector

@ReprInjector.withParent(('getVehicleInventoryID', 'vInvID'), ('getWaitingID', 'waitingID'))

class RankedQueueCtx(QueueCtx):
    """
    Enqueue ranked request context
    """

    def __init__(self, vInventoryID, waitingID = ''):
        super(RankedQueueCtx, self).__init__(entityType=QUEUE_TYPE.RANKED, waitingID=waitingID)
        self.__vInventoryID = vInventoryID

    def getVehicleInventoryID(self):
        """
        Gets selected vehicle inventory ID
        """
        return self.__vInventoryID