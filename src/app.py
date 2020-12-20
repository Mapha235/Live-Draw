from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QPen


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.main_widget = QWidget()

        self.drawing = False
        self.lastPoint = QPoint()

        screen = QApplication.primaryScreen()
        self.image = screen.grabWindow(0)

        self.setGeometry(0, 0, self.image.width(), self.image.height())
        self.showFullScreen()

        self.setCentralWidget(self.main_widget)

    def initUI(self):
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False
