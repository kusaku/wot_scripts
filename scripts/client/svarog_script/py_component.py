# Embedded file name: scripts/client/svarog_script/py_component.py
import Svarog
from svarog_script.auto_properties import AutoPropertyInitMetaclass

class Component(object):
    __metaclass__ = AutoPropertyInitMetaclass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def destroy(self):
        pass