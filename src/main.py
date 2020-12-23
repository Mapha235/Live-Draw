import sys
import os
from PyQt5 import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication, QPixmap
from PyQt5.QtCore import QFile, QIODevice, QPoint, QRect, QSize

import keyboard
import pyautogui
from PIL import ImageGrab

from app import Window
from screenAnalyzer import Analyzer

def main():
    app = QApplication(sys.argv)

    analyzer = Analyzer()
    analyzer.analyzeScreenOrder()
    print(analyzer.getZeroPoint())

    keyboard.wait('Ctrl+b')
    im = None
    screenshot = pyautogui.press("printscreen")
    im = ImageGrab.grabclipboard()
    im.save('./temp.png')

    screen = QGuiApplication.primaryScreen()
    
    rect = QRect(analyzer.getZeroPoint(), analyzer.getZeroPoint() + QPoint(screen.size().width(), screen.size().height()))

    image = QPixmap("./temp.png")
    cropped_image = image.copy(rect)

    os.system("del /f temp.png")

    window = Window(cropped_image)
    window.initUI()
    window.signalHandler()
    window.showFullScreen()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
