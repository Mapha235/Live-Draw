from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton,  QVBoxLayout
from PyQt5.QtCore import QEvent, QSize, Qt
from PyQt5 import QtGui
from settings import Settings


class Tools(QWidget):
    def __init__(self, parent = None):
        super(Tools, self).__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.eraser_btn = QPushButton("Erase")
        # self.eraser_btn.setFixedSize(20, 20)

        self.save_btn = QPushButton()
        self.save_btn.setFixedSize(30, 30)
        self.save_btn.setIcon(QtGui.QIcon(QtGui.QIcon("./data/save_icon.png")))
        self.save_btn.setIconSize(QSize(30, 30))

        self.settings_btn = QPushButton()
        self.settings_btn.setFixedSize(30, 30)
        self.settings_btn.setIcon(QtGui.QIcon(
            QtGui.QIcon("./data/settings.png")))
        self.settings_btn.setIconSize(QSize(15, 15))

        # ------------ Color palette --------------
        self.red_btn = QPushButton()
        self.red_btn.setFixedSize(20, 20)
        self.red_btn.setStyleSheet("background-color: red")
        self.red_btn.installEventFilter(self)

        self.green_btn = QPushButton()
        self.green_btn.setFixedSize(20, 20)
        self.green_btn.setStyleSheet("background-color: green")
        self.green_btn.installEventFilter(self)

        self.blue_btn = QPushButton()
        self.blue_btn.setFixedSize(20, 20)
        self.blue_btn.setStyleSheet("background-color: blue")
        self.blue_btn.installEventFilter(self)

        self.yellow_btn = QPushButton()
        self.yellow_btn.setFixedSize(20, 20)
        self.yellow_btn.setStyleSheet("background-color: yellow")
        self.yellow_btn.installEventFilter(self)

        self.black_btn = QPushButton()
        self.black_btn.setFixedSize(20, 20)
        self.black_btn.setStyleSheet("background-color: black")
        self.black_btn.installEventFilter(self)

        self.white_btn = QPushButton()
        self.white_btn.setFixedSize(20, 20)
        self.white_btn.setStyleSheet("background-color: white")
        self.white_btn.installEventFilter(self)

        self.color_btns = [self.red_btn, self.green_btn, self.blue_btn,
                           self.yellow_btn, self.black_btn, self.white_btn]
        self.btn_colors = [Qt.red, Qt.green, Qt.blue,
                           Qt.yellow, Qt.black, Qt.white]
        # -----------------------------------------
        self.default_theme = "border: 0px"
        self.current_selected = self.red_btn
        self.current_selected.setStyleSheet(self.default_theme)

        self.tools = QWidget()
        self.colors = QWidget()
        self.menu = QWidget()

        self.signalHandler()

    def initUI(self):
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(0)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setAlignment(Qt.AlignRight)
        menu_layout.addWidget(self.save_btn)
        menu_layout.addWidget(self.settings_btn)
        self.menu.setLayout(menu_layout)

        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(0)
        tools_layout.setContentsMargins(0, 0, 0, 0)
        tools_layout.setAlignment(Qt.AlignHCenter)
        tools_layout.addWidget(self.eraser_btn)
        self.tools.setLayout(tools_layout)

        colors_layout = QHBoxLayout()
        colors_layout.setAlignment(Qt.AlignHCenter)
        colors_layout.setSpacing(0)
        colors_layout.setContentsMargins(0, 0, 0, 0)
        colors_layout.addWidget(self.black_btn)
        colors_layout.addWidget(self.white_btn)
        colors_layout.addWidget(self.red_btn)
        colors_layout.addWidget(self.green_btn)
        colors_layout.addWidget(self.blue_btn)
        colors_layout.addWidget(self.yellow_btn)
        self.colors.setLayout(colors_layout)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.menu)
        main_layout.addWidget(self.tools)
        main_layout.addWidget(self.colors)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def signalHandler(self):
        # self.settings_btn.clicked.connect(self.openSettings)
        pass    

    def eventFilter(self, obj, event):
        # if(event.type() == QEvent.MouseButtonPress):
        #     self.current_selected.setStyleSheet(self.default_theme)
        #     if(type(obj) is QPushButton):
        #         obj.setStyleSheet("""border: 2px solid rgb(0, 100, 255)""")
        #         self.current_selected = obj

        return super(Tools, self).eventFilter(obj, event)
