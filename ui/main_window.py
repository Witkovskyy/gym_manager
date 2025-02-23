from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class GymApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Obsługi Siłowni")
        self.setFixedWidth(600)
        self.setFixedHeight(400)

        
        layout = QVBoxLayout()
        self.button = QPushButton("Dodaj klienta")
        layout.addWidget(self.button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

app = QApplication([])
window = GymApp()
window.show()
app.exec()