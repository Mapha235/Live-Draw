from PyQt5.QtCore import QFile, QIODevice, QPoint, QRect, QSize, QTimer, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QMainWindow, QPushButton, QShortcut, QWidget
from PyQt5.QtGui import QColor, QGuiApplication, QImage, QKeySequence, QPainter, QPen, QPixmap, QPalette

from tools import Tools
from settings import Settings

import keyboard
from PIL import ImageGrab
import os

color_dictionary = {
    Qt.blue: "blue",
    Qt.red: "red",
    Qt.yellow: "yellow",
    Qt.green: "rgb(0,255,0)",
    Qt.white: "white",
    Qt.black: "black"
}


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        # self.setWindowFlag(Qt.FramelessWindowHint)

        self.settings = None
        self.image = None

        self.history = []
        self.line = Line()

        self.eraser_size = 5
        self.is_eraser = False
        self.eraser_rect = QRect(QPoint(), QSize())

        self.initialized = False

        self.main_widget = QWidget()
        self.btn = QPushButton("Press me")

        self.pen_color = Qt.red
        self.drawing = False
        self.lastPoint = QPoint()

        self.setCentralWidget(self.main_widget)

        # -------------------------- Shortcuts ------------------------------
        self.start_key_seq = "Ctrl+U"
        self.hide_key_seq = "Ctrl+H"
        self.keystroke_counter = 0

        self.close_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)

        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.current_history_index = 0

        self.redo_shortcut = QShortcut(QKeySequence("Ctrl+Y"), self)

        # -------------------------------------------------------------------

        timer = QTimer(self)
        timer.timeout.connect(self.checkShortcuts)
        timer.start(1)

    def initUI(self):
        self.tools = Tools(QRect(self.width()/2 - 150, 0, 300, 50))
        self.tools.initUI()

        self.main_layout = QGridLayout()

        self.main_widget.setLayout(self.main_layout)

        self.initialized = True

    def signalHandler(self):
        self.tools.save_btn.clicked.connect(self.save)
        self.tools.green_btn.clicked.connect(lambda: self.setColor(Qt.green))
        self.tools.blue_btn.clicked.connect(lambda: self.setColor(Qt.blue))
        self.tools.red_btn.clicked.connect(lambda: self.setColor(Qt.red))
        self.tools.yellow_btn.clicked.connect(lambda: self.setColor(Qt.yellow))
        self.tools.black_btn.clicked.connect(lambda: self.setColor(Qt.black))
        self.tools.white_btn.clicked.connect(lambda: self.setColor(Qt.white))

        self.tools.eraser_btn.clicked.connect(self.toggleEraser)
        self.tools.eraser_dropdown.currentTextChanged.connect(
            self.setEraserSize)
        self.tools.erase_all_btn.clicked.connect(self.clearAll)
        self.tools.settings_btn.clicked.connect(self.openSettings)

        self.close_shortcut.activated.connect(self.closeApp)
        self.save_shortcut.activated.connect(self.save)
        self.undo_shortcut.activated.connect(self.undo)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.canvas)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.canvas)
            if self.is_eraser:
                r = QRect(QPoint(), self.eraser_size*QSize(1, 1))
                r.moveCenter(event.pos())
                px = self.image.copy(r)
                painter.save()
                painter.eraseRect(r)
                painter.restore()
                painter.drawPixmap(r, px)
            else:
                painter.setPen(
                    QPen(self.pen_color, self.eraser_size, Qt.SolidLine))
                painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

        # TODO
        self.history = self.history[0:self.current_history_index+1]
        self.history.append(self.canvas.copy())
        self.current_history_index += 1

    def clearAll(self):
        self.canvas = self.image.copy(
            QRect(0, 0, self.image.width(), self.image.height()))
        self.update()

    def setEraserSize(self, size):
        self.eraser_size = int(size)

    def setColor(self, color):
        self.pen_color = color
        pal = self.tools.selected_btn.palette()
        pal.setColor(QPalette.Button, color)
        self.tools.selected_btn.setAutoFillBackground(True)
        self.tools.selected_btn.setStyleSheet(
            "background-color: " + color_dictionary[color])
        self.tools.selected_btn.setPalette(pal)
        self.tools.selected_btn.update()
        self.is_eraser = False

    def toggleEraser(self):
        self.is_eraser = not self.is_eraser

    def makeScreenshot(self):
        im = ImageGrab.grab()
        im.save('./temp.png')

        self.image = QPixmap("./temp.png")
        self.history.append(self.image.copy())
        self.current_history_index = len(self.history) - 1

        self.setGeometry(0, 0, self.image.width(), self.image.height())
        self.canvas = self.image.copy(
            QRect(0, 0, self.image.width(), self.image.height()))
        os.system("del /f temp.png")

        if self.initialized is False:
            self.initUI()
            self.signalHandler()
            self.showApp()
        else:
            self.hideApp()
            self.showApp()

    def showApp(self):
        if self.settings is not None:
            self.settings.show()
        self.tools.show()
        self.show()
        self.showFullScreen()

    def hideApp(self):
        if self.settings is not None:
            self.settings.hide()
        self.tools.hide()
        self.hide()

    def checkShortcuts(self):
        upper_bound = 1

        if keyboard.is_pressed(self.start_key_seq):
            self.keystroke_counter += 1

            if(self.keystroke_counter == upper_bound):
                self.makeScreenshot()

        elif keyboard.is_pressed(self.hide_key_seq):
            self.keystroke_counter += 1

            if(self.keystroke_counter == upper_bound):
                if self.isVisible():
                    self.hideApp()
                else:
                    self.showApp()

            elif self.keystroke_counter > upper_bound:
                self.keystroke_counter = upper_bound

        else:
            self.keystroke_counter = 0

    def closeApp(self):
        if self.settings is not None:
            self.settings.close()
        self.tools.close()
        self.close()

    def openSettings(self):
        self.settings = Settings()
        self.settings.initUI()
        self.settings.show()

    def save(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                               "/untitled.png",
                                               "Images (*.png *.xpm *.jpg)")
        file = QFile(fileName[0])

        file.open(QIODevice.WriteOnly)
        self.canvas.save(file, "PNG")

    def undo(self):
        if self.current_history_index > 0:
            self.current_history_index -= 1
            self.canvas = self.history[self.current_history_index].copy()
            self.repaint()
