from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QGuiApplication, QScreen
from PyQt5.QtCore import QPoint


class Analyzer(QMainWindow):
    def __init__(self):
        super(Analyzer, self).__init__()

        self.zero_point = QPoint(0, 0)
        self.show()

    def analyzeScreenOrder(self):
        primary_screen = QGuiApplication.primaryScreen()
        primary_screen_size = primary_screen.availableSize()

        screens = QGuiApplication.screens()

        for screen_index in range(1, len(screens)):
            # screens[screen_index]
            self.windowHandle().setScreen(screens[screen_index])
            self.showFullScreen()
            self.hide()
            # print(self.x())

            if(self.x() < 0):
                self.zero_point -= QPoint(self.x(), 0)

            if(self.y() < 0):
                self.zero_point -= QPoint(0, self.y())

    def getZeroPoint(self):
        return self.zero_point
