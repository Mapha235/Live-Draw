from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen

from tools import Tools

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.pen_color = Qt.red

        self.main_widget = QWidget()
        self.btn = QPushButton("Press me")
        self.drawing = False
        self.lastPoint = QPoint()

        screen = QApplication.primaryScreen()
        self.image = screen.grabWindow(0)

        self.setGeometry(0, 0, self.image.width(), self.image.height())
        self.showFullScreen()

        self.setCentralWidget(self.main_widget)

        self.tools = Tools()
        self.tools.initUI()
        self.tools.show()
        self.tools.blue_btn.clicked.connect(lambda: self.setColor(Qt.blue))
        self.tools.red_btn.clicked.connect(lambda: self.setColor(Qt.red))

    def initUI(self):
        self.main_layout = QGridLayout()
        # self.main_layout.addWidget(self.btn, 0, 0, 1, 1)
        # self.main_layout.addWidget(self.tools, 0, 0, 1, 1)
        # self.main_layout.addWidget(self.image, 1, 0, 1, 1)
        
        # self.bg = QImage()
        # scaled_bg = self.bg.scaled(QSize(self.my_width, self.my_height))
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        # self.setPalette(palette)

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
            painter.setPen(QPen(self.pen_color, 3, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def setColor(self, color):
        self.pen_color = color