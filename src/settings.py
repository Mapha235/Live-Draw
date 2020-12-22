from PyQt5.QtWidgets import QPushButton, QLabel, QWidget, QLineEdit, QGridLayout
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeyEvent


class Settings(QWidget):
    def __init__(self):
        super(Settings, self).__init__()
        self.default_theme = self.styleSheet()

        self.save_label = QLabel("Save")
        self.hide_label = QLabel("Hide")
        self.close_label = QLabel("Close")
        self.start_label = QLabel("Start")

        self.save_line = QLineEdit("Ctrl+S")
        self.save_line.setReadOnly(True)
        self.save_line.setAlignment(Qt.AlignHCenter)
        self.save_line.installEventFilter(self)

        self.hide_line = QLineEdit("Ctrl+H")
        self.hide_line.setReadOnly(True)
        self.hide_line.setAlignment(Qt.AlignHCenter)
        self.hide_line.installEventFilter(self)

        self.close_line = QLineEdit("Esc")
        self.close_line.setReadOnly(True)
        self.close_line.setAlignment(Qt.AlignHCenter)
        self.close_line.installEventFilter(self)

        self.start_line = QLineEdit("Ctrl+B")
        self.start_line.setReadOnly(True)
        self.start_line.setAlignment(Qt.AlignHCenter)
        self.start_line.installEventFilter(self)

        self.current_selected = self.start_line

    def initUI(self):
        layout = QGridLayout()
        layout.addWidget(self.start_label, 0, 0, 1, 1)
        layout.addWidget(self.start_line, 0, 1, 1, 1)
        layout.addWidget(self.close_label, 1, 0, 1, 1)
        layout.addWidget(self.close_line, 1, 1, 1, 1)
        layout.addWidget(self.hide_label, 2, 0, 1, 1)
        layout.addWidget(self.hide_line, 2, 1, 1, 1)
        layout.addWidget(self.save_label, 3, 0, 1, 1)
        layout.addWidget(self.save_line, 3, 1, 1, 1)
        self.setLayout(layout)
        # layout.addWidget(self.)
        # layout.addWidget(self.)

    def eventFilter(self, obj, event):
        if(event.type() == QEvent.MouseButtonPress):
            self.current_selected.setStyleSheet(self.default_theme)
            if(type(obj) is QLineEdit):
                obj.setStyleSheet("""border: 2px solid rgb(0, 100, 255)""")
                self.current_selected = obj

        elif (event.type() == QEvent.KeyPress):
            key = QKeyEvent(event)
            self.current_selected.setText(key.text())
        # else:
        #     return super(Settings, self).eventFilter(obj, event)

        return super(Settings, self).eventFilter(obj, event)
