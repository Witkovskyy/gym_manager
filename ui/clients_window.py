import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStatusBar, QDialog, QLabel
from PyQt6.QtWidgets import QSpinBox, QLineEdit, QTextEdit, QComboBox, QGridLayout
from PyQt6.QtGui import QAction 
from datetime import date

class AddClientPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dodaj klienta")
        self.setGeometry(200,200,400,600)

        # add_client_layout = QVBoxLayout()
        add_client_layout = QGridLayout()


        # Inputy do wprowadzania danych klienta
        self.label = QLabel("Panel dodawania klienta")
        add_client_layout.addWidget(self.label)
        (self.label, 0, 0)

        #Rodo
        self.label = QLabel("Czy jest rodo", self)
        add_client_layout.addWidget(self.label, 1, 0)

        # self.label.move(50,50)
        # self.combo_box.setGeometry(50, 50, 150, 30)

      
        # self.combo_box = QComboBox(self)

        #Imię
        self.label = QLabel("Imię", self)
        add_client_layout.addWidget(self.label, 2, 0)

        # self.label.move(50,50)

        self.text_input = QLineEdit(self)
        add_client_layout.addWidget(self.text_input, 3, 0)
        # self.text_input.setGeometry(50, 70, 200, 30)

        #Nazwisko
        self.label = QLabel("Nazwisko", self)
        add_client_layout.addWidget(self.label, 4, 0)
        # self.label.move(50,110)

        self.text_input = QLineEdit(self)
        add_client_layout.addWidget(self.text_input, 5, 0)
        # self.text_input.setGeometry(50, 130, 200, 30)


        self.setLayout(add_client_layout)


