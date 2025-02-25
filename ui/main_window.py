import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStatusBar
from PyQt6.QtGui import QAction
from datetime import date

class GymApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Obsługi Siłowni")
        self.setGeometry(100,100,600,400)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Plik")

        exit_action = QAction("Zamknij", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage(f"{date.today().strftime("%d-%m-%Y")}")

        layout = QVBoxLayout()

        self.button = QPushButton("Dodaj klienta")
        layout.addWidget(self.button)

        self.button = QPushButton("Usuń klienta")
        layout.addWidget(self.button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

app = QApplication([])
window = GymApp()
window.show()
app.exec()