# Embedded file name: scripts/client/Helpers/PyGUI/Window.py
import BigWorld, GUI, Keys
from PyGUIBase import PyGUIBase
from DraggableComponent import DraggableComponent

class Window(PyGUIBase):
    factoryString = 'PyGUI.Window'

    def __init__(self, component):
        PyGUIBase.__init__(self, component)

    def onSave(self, dataSection):
        PyGUIBase.onSave(self, dataSection)

    def onLoad(self, dataSection):
        PyGUIBase.onLoad(self, dataSection)

    @staticmethod
    def create(texture):
        c = GUI.Window(texture)
        s = Window(c)
        s.onBound()
        return c


class EscapableWindow(Window):
    factoryString = 'PyGUI.EscapableWindow'

    def __init__(self, component = None):
        Window.__init__(self, component)
        self.onEscape = None
        return

    def handleKeyEvent(self, event):
        if event.isKeyDown():
            if event.key == Keys.KEY_ESCAPE:
                if self.onEscape is not None:
                    self.onEscape()
                    return True
        return False


class DraggableWindow(Window, DraggableComponent):
    factoryString = 'PyGUI.DraggableWindow'

    def __init__(self, component, horzDrag = True, vertDrag = True, restrictToParent = True):
        Window.__init__(self, component)
        DraggableComponent.__init__(self, horzDrag, vertDrag, restrictToParent)
        self.onBeginDrag = self._onBeginDrag

    def handleMouseButtonEvent(self, comp, event):
        return DraggableComponent.handleMouseButtonEvent(self, comp, event)

    def onSave(self, dataSection):
        DraggableComponent.onSave(self, dataSection)
        Window.onSave(self, dataSection)

    def onLoad(self, dataSection):
        DraggableComponent.onLoad(self, dataSection)
        Window.onLoad(self, dataSection)

    def _onBeginDrag(self):
        self.listeners.onBeginDrag()

    @staticmethod
    def create(texture):
        c = GUI.Window(texture)
        s = DraggableWindow(c)
        s.onBound()
        return c