from PyQt5.QtCore import QFile, QIODevice, QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QMainWindow, QPushButton, QShortcut, QWidget
from PyQt5.QtGui import QColor, QImage, QKeySequence, QPainter, QPen, QPixmap

from tools import Tools
from settings import Settings

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.settings = None

        self.is_eraser = False
        self.eraser_rect = QRect(QPoint(), QSize())

        self.pen_color = Qt.red

        self.main_widget = QWidget()
        self.btn = QPushButton("Press me")
        self.drawing = False
        self.lastPoint = QPoint()

        screen = QApplication.primaryScreen()
        self.image = screen.grabWindow(0)

        self.setGeometry(0, 0, self.image.width(), self.image.height())
        self.showFullScreen()

        self.canvas = self.image.copy(
            QRect(0, 0, self.image.width(), self.image.height()))

        self.setCentralWidget(self.main_widget)

        self.tools = Tools()
        self.tools.initUI()
        self.tools.show()

        # ------------ Shortcuts ----------------
        self.start_shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        self.hide_shortcut = QShortcut(QKeySequence("Ctrl+H"), self)
        self.close_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        # ---------------------------------------

    def initUI(self):
        self.main_layout = QGridLayout()

        self.main_widget.setLayout(self.main_layout)

    def signalHandler(self):
        self.tools.save_btn.clicked.connect(self.save)
        self.tools.green_btn.clicked.connect(lambda: self.setColor(Qt.green))
        self.tools.blue_btn.clicked.connect(lambda: self.setColor(Qt.blue))
        self.tools.red_btn.clicked.connect(lambda: self.setColor(Qt.red))
        self.tools.yellow_btn.clicked.connect(lambda: self.setColor(Qt.yellow))
        self.tools.black_btn.clicked.connect(lambda: self.setColor(Qt.black))
        self.tools.white_btn.clicked.connect(lambda: self.setColor(Qt.white))
        self.tools.eraser_btn.clicked.connect(self.toggle)
        self.tools.settings_btn.clicked.connect(self.openSettings)

        self.start_shortcut.activated.connect(lambda: print("start"))
        self.hide_shortcut.activated.connect(lambda: print("hide"))
        self.close_shortcut.activated.connect(self.closeApp)
        self.save_shortcut.activated.connect(self.save)

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
                r = QRect(QPoint(), 100*QSize(1, 1))
                r.moveCenter(event.pos())
                px = self.image.copy(r)
                painter.save()
                painter.eraseRect(r)
                painter.restore()
                painter.drawPixmap(r, px)
            else:
                painter.setPen(QPen(self.pen_color, 3, Qt.SolidLine))
                painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def setColor(self, color):
        self.pen_color = color
        self.is_eraser = False

    def toggle(self):
        self.is_eraser = not self.is_eraser

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
                                               "/home/jana/untitled.png",
                                               "Images (*.png *.xpm *.jpg)")
        file = QFile(fileName[0])

        file.open(QIODevice.WriteOnly)
        self.canvas.save(file, "PNG")
