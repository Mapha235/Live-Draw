from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QPushButton
from PyQt5.QtGui import QColor, QImage, QPainter, QPen, QPixmap

from tools import Tools


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

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
        self.tools.blue_btn.clicked.connect(lambda: self.setColor(Qt.blue))
        self.tools.red_btn.clicked.connect(lambda: self.setColor(Qt.red))
        self.tools.eraser_btn.clicked.connect(self.toggle)

    def initUI(self):
        self.main_layout = QGridLayout()

        self.main_widget.setLayout(self.main_layout)

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
                r = QRect(QPoint(), 20*QSize(1, 1))
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
