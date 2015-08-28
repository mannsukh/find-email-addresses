#!/usr/bin/env python

import sys
import re
import signal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebPage

## Class from http://webscraping.com/blog/Scraping-multiple-JavaScript-webpages-with-webkit/

class Render(QWebPage):
    def __init__(self, url):
        # Avoiding css and js file
        if re.search(r'\.js$|\.css$', url) is None:
            self.parsedEmails = []

            self.app = QApplication.instance()
            if self.app is None:
                self.app = QApplication(sys.argv)

            QWebPage.__init__(self)
            self.html = None
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            self.connect(self, SIGNAL('loadFinished(bool)'), self._finished_loading)
            self.mainFrame().load(QUrl(url))
            self.app.exec_()

    def _finished_loading(self, result):
        self.html = self.mainFrame().toHtml().toUtf8()
        self.app.quit()
