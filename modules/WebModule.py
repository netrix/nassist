__author__ = 'Netrix'
import PyQt5.QtCore as qtcore
import PyQt5.QtWebKitWidgets as qtwebkit
from modules.BaseModule import BaseModule

class WebModule(BaseModule):
    name = "ap"

    def __init__(self, parent):
        super(WebModule, self).__init__(parent)
        self.__result = qtwebkit.QWebView()
        self.__result.loadFinished.connect(self.__loadingFinished)
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

    def __loadingFinished(self):
        frame = self.__result.page().mainFrame()
        self.__result.page().setViewportSize(frame.contentsSize())
        self.__result.resize(frame.contentsSize())

