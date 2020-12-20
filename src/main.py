import sys
from PyQt5 import *
from PyQt5.QtWidgets import QApplication
from app import Window

def main():
    app = QApplication(sys.argv)
    window = Window()
    
    # window.setWindowOpacity(0.2)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()