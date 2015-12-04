__author__ = 'Netrix'
from modules.WebModule import WebModule

class SjpModule(WebModule):
    name = "sjp"

    def __init__(self, parent):
        super(SjpModule, self).__init__(parent)

    def getPreloadUrl(self):
        return "http://sjp.pl/"

    def createUrl(self, text):
        return "http://sjp.pl/{}".format(text)
