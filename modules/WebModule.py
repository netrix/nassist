__author__ = 'Netrix'
import PyQt5.QtCore as qtcore
import PyQt5.QtWebEngineWidgets as qtwebkit
from modules.BaseModule import BaseModule


class WebModule(BaseModule):
    name = "ap"

    def __init__(self, parent):
        super(WebModule, self).__init__(parent)
        self.__result = qtwebkit.QWebEngineView()
        self.__result.setEnabled(False)
        self.__result.loadFinished.connect(self.__loading_finished)
        self.__result.load(qtcore.QUrl(self.getPreloadUrl()))  # preload

    def getPreloadUrl(self):
        raise "Not implemented"

    def createUrl(self, text):
        raise "Not implemented"

    def onKeyPress(self, event):
        pass

    def onTextUpdate(self, text):
        self.__result.load(qtcore.QUrl(self.createUrl(text)))

    def onActivate(self):
        self.parent.addWidget(self.__result)
        self.__result.show()

    def onDeactivate(self):
        self.__result.setParent(None)

    def __loading_finished(self):
        pass
