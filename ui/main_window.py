import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStatusBar, QDialog, QLabel
from PyQt6.QtWidgets import QSpinBox, QLineEdit, QTextEdit, QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QAction 
from datetime import date
from ui.clients_window import AddClientPopup, DelClientPopup

class GymManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Obsługi Siłowni")
        self.setGeometry(100,100,1400,600)

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
        self.button.clicked.connect(self.show_del_client)
        layout.addWidget(self.button)

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
        layout.addWidget(self.table_view)
        
        container = QWidget()
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