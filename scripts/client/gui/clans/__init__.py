# Embedded file name: scripts/client/gui/clans/__init__.py
from skeletons.gui.clans import IClanController
__all__ = ('getClanServicesConfig',)

def getClanServicesConfig(manager):
    """ Configures services for package clans.
    :param manager: helpers.dependency.DependencyManager
    """
    from gui.clans.clan_controller import ClanController
    ctrl = ClanController()
    ctrl.init()
    manager.addInstance(IClanController, ctrl, finalizer='fini')