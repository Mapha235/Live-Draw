from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton,  QVBoxLayout
from PyQt5.QtCore import Qt


class Tools(QWidget):
    def __init__(self):
        super(Tools, self).__init__()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.pen_btn = QPushButton("Pen")
        self.pen_btn.setFixedSize(20,20)

        self.eraser_btn = QPushButton("Erase")
        self.eraser_btn.setFixedSize(20,20)

        self.blue_btn = QPushButton("Blue")
        self.blue_btn.setFixedSize(20,20)

        self.red_btn = QPushButton("Red")
        self.red_btn.setFixedSize(20,20)

        self.tools = QWidget()
        self.colors = QWidget()

    def initUI(self):
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(0)
        tools_layout.setContentsMargins(0, 0, 0, 0)
        tools_layout.setAlignment(Qt.AlignHCenter)
        tools_layout.addWidget(self.pen_btn)
        tools_layout.addWidget(self.eraser_btn)
        self.tools.setLayout(tools_layout)

        colors_layout = QHBoxLayout()
        colors_layout.setAlignment(Qt.AlignHCenter)
        colors_layout.setSpacing(0)
        colors_layout.setContentsMargins(0, 0, 0, 0)
        colors_layout.addWidget(self.blue_btn)
        colors_layout.addWidget(self.red_btn)
        self.colors.setLayout(colors_layout)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.tools)
        main_layout.addWidget(self.colors)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def signalHandler(self):
        # self.blue_btn.clicked.connect()
        pass
