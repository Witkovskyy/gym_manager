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
from contextlib import contextmanager

@contextmanager
def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
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
    
    def getMembershipDuration(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        stmt = select(Membership)
        membership_obj = session.scalars(stmt).all()
        # print(membership_obj)
        membership_duration = [m.membership_duration_in_days for m in membership_obj]

        # print(membership_obj)
        session.close()
        return membership_duration

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
        add_client_layout.addWidget(QLabel("Panel dodawania klienta"), 0, 0)

        #Rodo
        self.label_is_rodo = QLabel("Czy jest rodo", self)
        add_client_layout.addWidget(self.label_is_rodo , 1, 0)

        self.combo_box_rodo = QComboBox(self)
        add_client_layout.addWidget(self.combo_box_rodo, 2, 0)
        self.combo_box_rodo.addItems(["Tak", "Nie"])
        self.combo_box_rodo.setCurrentText("Tak")

        #Nieletni
        self.label_is_underage = QLabel("Czy klient jest nieletni", self)
        add_client_layout.addWidget(self.label_is_underage, 3, 0)

        self.combo_box_underage = QComboBox(self)
        add_client_layout.addWidget(self.combo_box_underage, 4, 0)
        self.combo_box_underage.addItems(["Nie", "Tak"])
        self.combo_box_underage.setCurrentText("Nie")

        #Imię
        self.label_client_name = QLabel("Imię", self)
        add_client_layout.addWidget(self.label_client_name, 5, 0)

        # self.label.move(50,50)

        self.text_input_name = QLineEdit(self)
        add_client_layout.addWidget(self.text_input_name, 6, 0)
        # self.text_input.setGeometry(50, 70, 200, 30)

        #Nazwisko
        self.label_client_last_name = QLabel("Nazwisko", self)
        add_client_layout.addWidget(self.label_client_last_name, 7, 0)
        # self.label.move(50,110)

        self.text_input_last_name = QLineEdit(self)
        add_client_layout.addWidget(self.text_input_last_name, 8, 0)
        # self.text_input.setGeometry(50, 130, 200, 30)

        #Typ karnetu
        label_membership_type = QLabel("Wybierz typ karnetu", self)
        add_client_layout.addWidget(label_membership_type, 9, 0)

        
        self.combo_box_membership = QComboBox(self)
        add_client_layout.addWidget(self.combo_box_membership, 10, 0)
        memberships = MembershipsGetter().getMemberships()
        # print(memberships)
        if memberships:
            self.combo_box_membership.addItems(memberships)
            self.combo_box_membership.setCurrentText(memberships[0])
            self.combo_box_membership.currentTextChanged.connect(self.add_days)
        else:
            QMessageBox.warning(self, "Brak danych", "Brak dostępnych karnetów!")
            self.combo_box_membership.addItem("Brak")

        # Początek karnetu
        label_start_date = QLabel("Data początkowa karnetu", self)
        add_client_layout.addWidget(label_start_date, 11, 0)

        self.date_edit_start = QDateEdit()
        self.date_edit_start.setCalendarPopup(True)
        self.date_edit_start.setDate(QDate.currentDate())
        add_client_layout.addWidget(self.date_edit_start, 12, 0)
        self.date_edit_start.dateChanged.connect(self.add_days)

        # Koniec karnetu
        self.label_expiry_date = QLabel("Data końcowa karnetu", self)
        add_client_layout.addWidget(self.label_expiry_date, 13, 0)

        self.date_edit_expiry = QDateEdit()
        self.date_edit_expiry.setCalendarPopup(True)
        self.date_edit_expiry.setDate(QDate.currentDate().addDays(30))
        add_client_layout.addWidget(self.date_edit_expiry, 14, 0)

        # Komentarz do klienta
        self.label_comment = QLabel("Dodaj komentarz (opcjonalnie)", self)
        add_client_layout.addWidget(self.label_comment, 15, 0)
        self.text_input_comments = QLineEdit(self)
        self.text_input_comments.setText("Brak komentarza")
        add_client_layout.addWidget(self.text_input_comments, 16, 0)

        self.submit_button = QPushButton("Potwierdź dodanie")
        add_client_layout.addWidget(self.submit_button, 17, 0)
        self.submit_button.clicked.connect(self.validator)

        self.setLayout(add_client_layout)


    def add_days(self):

        start_date = self.date_edit_start.date()
        membership_type = self.combo_box_membership.currentText()
        
        if membership_type == "Półroczny":
            expiry_date = start_date.addDays(30)
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
        except Exception as e:
            print(f"Something went wrong. Can't save client info: {e}")

        session.close()

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
        label_delete_client = QLabel("Panel usuwania klienta")
        del_client_layout.addWidget(label_delete_client, 0, 0)

        label_client_name = QLabel("Imię klienta")
        del_client_layout.addWidget(label_client_name, 1, 0)

        self.text_input_name = QLineEdit(self)
        del_client_layout.addWidget(self.text_input_name, 2, 0)

        label_client_last_name = QLabel("Nazwisko klienta")
        del_client_layout.addWidget(label_client_last_name, 3, 0)

        self.text_input_last_name = QLineEdit(self)
        del_client_layout.addWidget(self.text_input_last_name, 4, 0)

        label_client_number = QLabel("Numer klienta")
        del_client_layout.addWidget(label_client_number, 5, 0)

        self.text_input_id = QLineEdit(self)
        del_client_layout.addWidget(self.text_input_id, 6, 0)

        submit_button = QPushButton("Potwierdź usunięcie")
        del_client_layout.addWidget(submit_button, 17, 0)
        submit_button.clicked.connect(self.delete_client)
        
        db = QSqlDatabase.database("main_connection")
        # self.db.setDatabaseName("gym_manager.db")

        if not db.open():
            print("Database connection failed!")

        self.table_view = QTableView()
        self.model = QSqlTableModel(None, db)
        self.model.setTable("clients")
        self.model.select()

        self.table_view.setModel(self.model)

        del_client_layout.addWidget(self.table_view, 8, 0)


        self.setLayout(del_client_layout)

    def delete_client(self):
        try:
            client_id = int(self.text_input_id.text())
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Numer klienta musi być liczbą")
            return

        with get_session() as session:
            stmt = select(Client).where(Client.client_id == client_id)
            client = session.scalars(stmt).first()

            if client:
                session.delete(client)
                QMessageBox.information(self, "Sukces", f"Klient o ID {client_id} został usunięty.")
                print(f"Client with id {client_id} deleted")
            else:
                QMessageBox.warning(self, "Nie znaleziono", f"Klient o ID {client_id} nie został znaleziony.")
                print(f"Client with id {client_id} not found")
