import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStatusBar, QDialog, QLabel
from PyQt6.QtWidgets import QSpinBox, QLineEdit, QTextEdit
from PyQt6.QtGui import QAction 
from datetime import date
from clients_window import AddClientPopup

# class AddClientPopup(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Dodaj klienta")
#         self.setGeometry(200,200,400,600)

#         add_client_layout = QVBoxLayout()

#         self.label = QLabel("Panel dodawania klienta")
#         add_client_layout.addWidget(self.label)

#         # Inputy do wprowadzania danych klienta

#         #Imię
#         self.label = QLabel("Imię", self)
#         self.label.move(50,50)

#         self.text_input = QLineEdit(self)
#         self.text_input.setGeometry(50, 80, 200, 30)

#         #Nazwisko




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

        # Status bar z datą w lewym dolnym
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage(f"{date.today().strftime("%d-%m-%Y")}")

        layout = QVBoxLayout()

        self.button = QPushButton("Dodaj klienta", self)
        self.button.clicked.connect(self.show_add_client)
        layout.addWidget(self.button)

        self.button = QPushButton("Usuń klienta")
        layout.addWidget(self.button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Funkcja wywołująca AddClientPopup
    def show_add_client(self):
        show_popup = AddClientPopup()
        show_popup.exec()


app = QApplication([])
window = GymApp()
window.show()
app.exec()