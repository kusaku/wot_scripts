# Embedded file name: scripts/common/items/components/gun_components.py
from collections import namedtuple
from items.components import legacy_stuff
RecoilEffect = namedtuple('RecoilEffect', ('lodDist', 'amplitude', 'backoffTime', 'returnTime'))

class GunShot(legacy_stuff.LegacyStuff):
    """Class contains configuration of gun shot. It's extended from LegacyStuff to make back capability
    to dictionary-like access when it needs."""
    __slots__ = ('shell', 'defaultPortion', 'piercingPower', 'speed', 'gravity', 'maxDistance', 'maxHeight')

    def __init__(self, shell, defaultPortion, piercingPower, speed, gravity, maxDistance, maxHeight):
        super(GunShot, self).__init__()
        self.shell = shell
        self.defaultPortion = defaultPortion
        self.piercingPower = piercingPower
        self.speed = speed
        self.gravity = gravity
        self.maxDistance = maxDistance
        self.maxHeight = maxHeight

    def __repr__(self):
        return 'GunShot(shell={}, portion={}, ppower={}, speed={}, gravity={}, max=({} distance, {} height))'.format(self.shell, self.defaultPortion, self.piercingPower, self.speed, self.gravity, self.maxDistance, self.maxHeight)

    def copy(self):
        raise AssertionError('Operation "GunShot.copy" is not allowed')