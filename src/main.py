import sys
import os
from PyQt5 import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication, QPixmap
from PyQt5.QtCore import QFile, QIODevice, QPoint, QRect, QSize

import keyboard
from PIL import ImageGrab

from app import Window


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
