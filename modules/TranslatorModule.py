__author__ = 'Netrix'
from modules.WebModule import WebModule

class TranslatorModule(WebModule):
    def __init__(self, parent, translate_from, translate_to):
        super(TranslatorModule, self).__init__(parent)
        self.translate_from = translate_from
        self.translate_to = translate_to

    def getPreloadUrl(self):
        return "https://translate.google.com/"

    def createUrl(self, text):
        return "https://translate.google.com/#{}/{}/{}".format(self.translate_from, self.translate_to, text)
