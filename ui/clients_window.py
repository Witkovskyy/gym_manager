import sys
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStatusBar, QDialog, QLabel
from PyQt6.QtWidgets import QSpinBox, QLineEdit, QTextEdit, QComboBox, QGridLayout, QDateEdit
from PyQt6.QtGui import QAction 
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from pathlib import Path
# parent_path = str(Path(__file__).resolve().parent.parent)
# sys.path.append(parent_path)
sys.path.append(str(Path(__file__).resolve().parent.parent))
from models.db_setup import engine, Membership, Client


class MembershipsGetter():
    def getMemberships(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        stmt = select(Membership)
        membership_obj = session.scalars(stmt).all()
        # print(membership_obj)
        membership_names = [m.membership_name for m in membership_obj]

        # print(membership_obj)
        session.close()
        return membership_names
class MembershipDurationGetter():
    def getMembershipDuration(self):


        return True

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
        self.combo_box_rodo.setCurrentText("Tak")

        #Nieletni
        self.label = QLabel("Czy klient jest nieletni", self)
        add_client_layout.addWidget(self.label, 3, 0)

        self.combo_box_underage = QComboBox(self)
        add_client_layout.addWidget(self.combo_box_underage, 4, 0)
        self.combo_box_underage.addItems(["Nie", "Tak"])
        self.combo_box_rodo.setCurrentText("Nie")


        #Imię
        self.label = QLabel("Imię", self)
        add_client_layout.addWidget(self.label, 5, 0)

        # self.label.move(50,50)

        self.text_input_name = QLineEdit(self)
        add_client_layout.addWidget(self.text_input_name, 6, 0)
        # self.text_input.setGeometry(50, 70, 200, 30)

        #Nazwisko
        self.label = QLabel("Nazwisko", self)
        add_client_layout.addWidget(self.label, 7, 0)
        # self.label.move(50,110)

        self.text_input_last_name = QLineEdit(self)
        add_client_layout.addWidget(self.text_input_last_name, 8, 0)
        # self.text_input.setGeometry(50, 130, 200, 30)

        #Typ karnetu
        self.label = QLabel("Wybierz typ karnetu", self)
        add_client_layout.addWidget(self.label, 9, 0)

        self.combo_box_membership = QComboBox(self)
        add_client_layout.addWidget(self.combo_box_membership, 10, 0)
        memberships = MembershipsGetter().getMemberships()
        # print(memberships)
        self.combo_box_membership.addItems(memberships)
        self.combo_box_rodo.setCurrentText(memberships[0])


        # Początek karnetu
        self.label = QLabel("Data początkowa karnetu", self)
        add_client_layout.addWidget(self.label, 11, 0)

        self.date_edit_start = QDateEdit()
        self.date_edit_start.setCalendarPopup(True)
        self.date_edit_start.setDate(QDate.currentDate())
        add_client_layout.addWidget(self.date_edit_start, 12, 0)
        self.date_edit_start.dateChanged.connect(self.add_days)

        # Koniec karnetu
        self.label = QLabel("Data końcowa karnetu", self)
        add_client_layout.addWidget(self.label, 13, 0)

        self.date_edit_expiry = QDateEdit()
        self.date_edit_expiry.setCalendarPopup(True)
        self.date_edit_expiry.setDate(QDate.currentDate().addDays(30))
        add_client_layout.addWidget(self.date_edit_expiry, 14, 0)

        # Komentarz do klienta
        self.label = QLabel("Dodaj komentarz (opcjonalnie)", self)
        add_client_layout.addWidget(self.label, 15, 0)
        self.text_input_comment = QLineEdit(self)
        self.text_input_comment.setText("Brak komentarza")
        add_client_layout.addWidget(self.text_input_comment, 16, 0)


        self.submit_button = QPushButton("Potwierdź dodanie")
        add_client_layout.addWidget(self.submit_button, 17, 0)
        self.submit_button.clicked.connect(self.submit_client)




        self.setLayout(add_client_layout)


    def add_days(self):
        start_date = self.date_edit_start.date()
        membership_type = self.combo_box_membership.currentText()
        if membership_type == "Półroczny":
            expiry_date = start_date.addDays(180)
        else:
            expiry_date = start_date.addDays(30)
        # return expiry_date
        self.date_edit_expiry.setDate(expiry_date) 

    def submit_client(self):

        is_rodo = self.combo_box_rodo.currentText()
        is_underage = self.combo_box_underage.currentText()
        first_name = self.text_input_name.text()
        last_name = self.text_input_last_name.text()
        membership_type = self.combo_box_membership.currentText()
        start_date = self.date_edit_start.date().toPyDate()
        print(f"Saving Date: {start_date}")
        expiry_date = self.date_edit_expiry.date().toPyDate()
        print(f"Saving Date: {expiry_date}")
        comment = self.text_input_comment.text()


        new_client = Client(is_rodo, is_underage, first_name, last_name, membership_type, start_date, expiry_date, comment)
        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(new_client)
        session.commit()
        print("Date saved to database successfully!")







        



        


