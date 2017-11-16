# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/leviathanPreview/__init__.py
from gui.Scaleform.framework.package_layout import PackageBusinessHandler
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import EVENT_BUS_SCOPE

def getContextMenuHandlers():
    return ()


def getViewSettings():
    return ()


def getBusinessHandlers():
    return (LeviathanPreviewPackageBusinessHandler(),)


class LeviathanPreviewPackageBusinessHandler(PackageBusinessHandler):

    def __init__(self):
        super(LeviathanPreviewPackageBusinessHandler, self).__init__((), APP_NAME_SPACE.SF_LOBBY, EVENT_BUS_SCOPE.LOBBY)