__author__ = 'Netrix'


class BaseModule:
    name = "exit"

    def __init__(self, parent):
        self.parent = parent

    def onKeyPress(self, event):
        pass

    def onTextUpdate(self, text):
        pass

    def onActivate(self):
        pass

    def onDeactivate(self):
        pass

    def onClose(self):
        pass
