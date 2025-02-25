import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStatusBar, QDialog, QLabel
from PyQt6.QtWidgets import QSpinBox, QLineEdit, QTextEdit, QComboBox, QGridLayout
from PyQt6.QtGui import QAction 
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from pathlib import Path
parent_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_path)
sys.path.append(str(Path(__file__).resolve().parent / "models"))
from db_setup import engine, Membership, membership


class MembershipsGetter():
    def getMemberships():
        Session = sessionmaker(bind=engine)
        session = Session()

        stmt = select(Membership.membership_name)
        membership_obj = session.scalars(stmt).all()
        print(membership_obj)

class AddClientPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dodaj klienta")
        self.setGeometry(200,200,400,600)

        # add_client_layout = QVBoxLayout()
        add_client_layout = QGridLayout()
        add_client_layout.setSpacing(0)
        add_client_layout.setContentsMargins(10, 10, 10, 10)


        # Inputy do wprowadzania danych klienta
        self.label = QLabel("Panel dodawania klienta")
        add_client_layout.addWidget(self.label)
        (self.label, 0, 0)

        #Rodo
        self.label = QLabel("Czy jest rodo", self)
        add_client_layout.addWidget(self.label, 1, 0)

        # self.label.move(50,50)
        # self.combo_box.setGeometry(50, 50, 150, 30)

        self.combo_box_rodo = QComboBox(self)
        add_client_layout.addWidget(self.combo_box_rodo, 2, 0)
        self.combo_box_rodo.addItems(["Tak", "Nie"])

        #Nieletni
        self.label = QLabel("Czy klient jest nieletni", self)
        add_client_layout.addWidget(self.label, 3, 0)

        self.combo_box_underage = QComboBox(self)
        add_client_layout.addWidget(self.combo_box_underage, 4, 0)
        self.combo_box_rodo.addItems(["Tak", "Nie"])

        #Imię
        self.label = QLabel("Imię", self)
        add_client_layout.addWidget(self.label, 5, 0)

        # self.label.move(50,50)

        self.text_input = QLineEdit(self)
        add_client_layout.addWidget(self.text_input, 6, 0)
        # self.text_input.setGeometry(50, 70, 200, 30)

        #Nazwisko
        self.label = QLabel("Nazwisko", self)
        add_client_layout.addWidget(self.label, 7, 0)
        # self.label.move(50,110)

        self.text_input = QLineEdit(self)
        add_client_layout.addWidget(self.text_input, 8, 0)
        # self.text_input.setGeometry(50, 130, 200, 30)

        #Typ karnetu
        self.label = QLabel("Wybierz typ karnetu", self)
        add_client_layout.addWidget(self.label, 9, 0)

        self.combo_box_membership = QComboBox(self)
        add_client_layout.addWidget(self.combo_box_membership, 10, 0)
        memberships = MembershipsGetter()
        self.combo_box_rodo.addItems(["Tak", "Nie"])



        self.setLayout(add_client_layout)



        


