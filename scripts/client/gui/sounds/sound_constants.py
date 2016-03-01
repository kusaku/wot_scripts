# Embedded file name: scripts/client/gui/sounds/sound_constants.py
from shared_utils import CONST_CONTAINER

class EnabledStatus(object):
    ENABLED_DEFAULT = 0
    ENABLED_BY_USER = 1
    DISABLED = 2

    @classmethod
    def isEnabled(cls, status):
        return status in (cls.ENABLED_DEFAULT, cls.ENABLED_BY_USER)


class HQRenderState(object):
    LQ_HQ_ENABLED = 0
    LQ_FOR_ALL = 1
    HQ_FOR_ALL = 2

    @classmethod
    def isEnabled(cls, status, isMSR):
        if status == cls.LQ_HQ_ENABLED:
            return not isMSR
        else:
            return status == cls.HQ_FOR_ALL


PLAYING_SOUND_CHECK_PERIOD = 1.0
IS_ADVANCED_LOGGING = False

class SoundSystems(CONST_CONTAINER):
    UNKNOWN = 0
    FMOD = 1
    WWISE = 2

    @classmethod
    def getUserName(cls, sysID):
        return cls.getKeyByValue(sysID) or cls.UNKNOWN


class SoundFilters(CONST_CONTAINER):
    EMPTY = 1
    FILTERED_HANGAR = 2
    FORT_FILTER = 3