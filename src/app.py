from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        
        self.setWindowTitle("Live Draw")
        self.showFullScreen()

        self.main_widget = QWidget()

        self.setCentralWidget(self.main_widget)
        

    def initUI(self):
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)
