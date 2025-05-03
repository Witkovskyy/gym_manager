import sys
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStatusBar, QDialog, QLabel
from PyQt6.QtWidgets import QTableView, QLineEdit, QTextEdit, QComboBox, QGridLayout, QDateEdit, QMessageBox
from PyQt6.QtGui import QAction 
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from pathlib import Path
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

# Dodawanie klienta do bazy
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

        combo_box_rodo = QComboBox(self)
        add_client_layout.addWidget(combo_box_rodo, 2, 0)
        combo_box_rodo.addItems(["Tak", "Nie"])
        combo_box_rodo.setCurrentText("Tak")

        #Nieletni
        label = QLabel("Czy klient jest nieletni", self)
        add_client_layout.addWidget(label, 3, 0)

        combo_box_underage = QComboBox(self)
        add_client_layout.addWidget(combo_box_underage, 4, 0)
        combo_box_underage.addItems(["Nie", "Tak"])
        combo_box_underage.setCurrentText("Nie")

        #Imię
        label = QLabel("Imię", self)
        add_client_layout.addWidget(label, 5, 0)

        # self.label.move(50,50)

        text_input_name = QLineEdit(self)
        add_client_layout.addWidget(text_input_name, 6, 0)
        # self.text_input.setGeometry(50, 70, 200, 30)

        #Nazwisko
        label = QLabel("Nazwisko", self)
        add_client_layout.addWidget(label, 7, 0)
        # self.label.move(50,110)

        text_input_last_name = QLineEdit(self)
        add_client_layout.addWidget(text_input_last_name, 8, 0)
        # self.text_input.setGeometry(50, 130, 200, 30)

        #Typ karnetu
        label = QLabel("Wybierz typ karnetu", self)
        add_client_layout.addWidget(label, 9, 0)

        combo_box_membership = QComboBox(self)
        add_client_layout.addWidget(combo_box_membership, 10, 0)
        memberships = MembershipsGetter().getMemberships()
        # print(memberships)
        combo_box_membership.addItems(memberships)
        combo_box_rodo.setCurrentText(memberships[0])
        combo_box_membership.currentTextChanged.connect(self.add_days)

        # Początek karnetu
        label = QLabel("Data początkowa karnetu", self)
        add_client_layout.addWidget(label, 11, 0)

        date_edit_start = QDateEdit()
        date_edit_start.setCalendarPopup(True)
        date_edit_start.setDate(QDate.currentDate())
        add_client_layout.addWidget(date_edit_start, 12, 0)
        date_edit_start.dateChanged.connect(self.add_days)

        # Koniec karnetu
        label = QLabel("Data końcowa karnetu", self)
        add_client_layout.addWidget(label, 13, 0)

        date_edit_expiry = QDateEdit()
        date_edit_expiry.setCalendarPopup(True)
        date_edit_expiry.setDate(QDate.currentDate().addDays(30))
        add_client_layout.addWidget(date_edit_expiry, 14, 0)

        # Komentarz do klienta
        label = QLabel("Dodaj komentarz (opcjonalnie)", self)
        add_client_layout.addWidget(label, 15, 0)
        text_input_comments = QLineEdit(self)
        text_input_comments.setText("Brak komentarza")
        add_client_layout.addWidget(text_input_comments, 16, 0)

        submit_button = QPushButton("Potwierdź dodanie")
        add_client_layout.addWidget(submit_button, 17, 0)
        submit_button.clicked.connect(self.validator)


        self.setLayout(add_client_layout)


    def add_days(self):

        start_date = self.date_edit_start.date()
        membership_type = self.combo_box_membership.currentText()
        if membership_type == "Półroczny":
            expiry_date = start_date.addDays(182)
        elif membership_type =="Roczny":
            expiry_date = start_date.addDays(365)
        else:
            expiry_date = start_date.addDays(30)
        self.date_edit_expiry.setDate(expiry_date) 

    def validator(self):

        first_name = self.text_input_name.text().strip()
        last_name = self.text_input_last_name.text().strip()

        if not first_name or not last_name:
            QMessageBox.warning(self, "Input Error", "Imię i nazwisko nie mogą być puste")
            return
        else:
            self.submit_client()

    def submit_client(self):

        is_rodo = self.combo_box_rodo.currentText()
        is_underage = self.combo_box_underage.currentText()
        first_name = self.text_input_name.text() 
        last_name = self.text_input_last_name.text()
        membership_type = self.combo_box_membership.currentText()
        start_date = self.date_edit_start.date().toPyDate()
        expiry_date = self.date_edit_expiry.date().toPyDate()
        comments = self.text_input_comments.text()

        new_client = Client(is_rodo, is_underage, first_name, last_name, membership_type, start_date, expiry_date, comments)
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            session.add(new_client)
            session.commit()
            print("Data saved to database successfully!")
        except:
            print("Something went wrong. Can't save client info")
        session.close()
        self.close()

# Usuwanie klienta z bazy
class DelClientPopup(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Usuń klienta")
        self.setGeometry(200,200,1000,500)

        del_client_layout = QGridLayout()
        del_client_layout.setSpacing(0)
        del_client_layout.setContentsMargins(10, 10, 10, 10)


        # Inputy do wprowadzania danych klienta
        label = QLabel("Panel usuwania klienta")
        del_client_layout.addWidget(label)
        del_client_layout.addWidget(label, 0, 0)

        label = QLabel("Imię klienta")
        del_client_layout.addWidget(label)
        del_client_layout.addWidget(label, 1, 0)

        text_input_name = QLineEdit(self)
        del_client_layout.addWidget(text_input_name)
        del_client_layout.addWidget(text_input_name, 2, 0)

        label = QLabel("Nazwisko klienta")
        del_client_layout.addWidget(label)
        del_client_layout.addWidget(label, 3, 0)

        text_input_last_name = QLineEdit(self)
        del_client_layout.addWidget(text_input_last_name)
        del_client_layout.addWidget(text_input_last_name, 4, 0)

        label = QLabel("Numer klienta")
        del_client_layout.addWidget(label)
        del_client_layout.addWidget(label, 5, 0)

        text_input_id = QLineEdit(self)
        del_client_layout.addWidget(text_input_id)
        del_client_layout.addWidget(text_input_id, 6, 0)

        submit_button = QPushButton("Potwierdź usunięcie")
        del_client_layout.addWidget(submit_button, 17, 0)
        submit_button.clicked.connect(self.delete_client)
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("gym_manager.db")
        self.db.open()

        if not self.db.open():
            print("Database connection failed!")

        self.table_view = QTableView()
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("clients")
        self.model.select()

        self.table_view.setModel(self.model)

        del_client_layout.addWidget(self.table_view, 8, 0)
        self.db.close()


        self.setLayout(del_client_layout)

    def delete_client(self):
        
        Session = sessionmaker(bind=engine)
        session = Session()
        client_name = self.text_input_name.text()
        client_last_name = self.text_input_last_name.text()
        client_id = self.text_input_id.text()

        stmt = select(Client).where(Client.client_id == client_id)
        client = session.scalars(stmt).first()
        try:
            if client:
                session.delete(client)
                session.commit()
                print(f"Client with id {client_id} deleted")
            else:
                print(f"Client with id {client_id} not found")
        except:
            print("Something went wrong")

        session.close()
