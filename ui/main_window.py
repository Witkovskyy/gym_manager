import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStatusBar, QDialog, QLabel
from PyQt6.QtWidgets import QSpinBox, QLineEdit, QTextEdit, QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer
from datetime import date
from ui.clients_window import AddClientPopup, DelClientPopup

class GymManager(QMainWindow):
    def refreshClients(self):
        self.model.select()

    def showClients(self, selfmodel, layout):
        selfmodel.setTable("clients")
        selfmodel.select()

        headers = ["ID", "RODO", "Nieletni", "Imie", "Nazwisko", "Rodzaj karnetu", "Początek karnetu", "Koniec karnetu", "Ostatnia wizyta", "Komentarz"]

        for i in range(len(headers)):
            selfmodel.setHeaderData(i, Qt.Orientation.Horizontal , headers[i])

        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refreshClients)
        self.refresh_timer.start(5000) 

    def createMainWindow(self):
        self.setWindowTitle("System Obsługi Siłowni")
        self.setGeometry(100,100,1400,600)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Plik")

        exit_action = QAction("Zamknij", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Status bar z datą w lewym dolnym
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage(f"{date.today().strftime('%d-%m-%Y')}")

        layout = QVBoxLayout()

        self.button = QPushButton("Dodaj klienta")
        self.button.clicked.connect(self.show_add_client)
        layout.addWidget(self.button)

        self.button = QPushButton("Usuń klienta")
        self.button.clicked.connect(self.show_del_client)
        layout.addWidget(self.button)

        self.refresh_button = QPushButton("Odśwież")
        self.refresh_button.clicked.connect(self.refreshClients)
        layout.addWidget(self.refresh_button)

        self.db = QSqlDatabase.addDatabase("QSQLITE", "main_connection")
        self.db.setDatabaseName("gym_manager.db")
        self.db.open()

        if not self.db.open():
            print("Database connection failed!")

        self.table_view = QTableView()
        self.model = QSqlTableModel(self, self.db)
        GymManager.showClients(self, self.model, layout)
        
        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

       

    # Funkcja wywołująca AddClientPopup
    def show_add_client(self):
        show_popup = AddClientPopup()
        show_popup.exec()
        
    # Funkcja wywołująca DelClientPopup
    def show_del_client(self):
        show_popup = DelClientPopup()
        show_popup.exec()

    

    #Init
    def __init__(self):
        super().__init__()
        self.createMainWindow()