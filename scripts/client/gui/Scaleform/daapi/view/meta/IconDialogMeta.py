# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/IconDialogMeta.py
from gui.Scaleform.daapi.view.dialogs.SimpleDialog import SimpleDialog

class IconDialogMeta(SimpleDialog):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends SimpleDialog
    null
    """

    def as_setIconS(self, path):
        """
        :param path:
        :return :
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setIcon(path)