import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from ui.main_window import GymManager

if __name__ == "__main__":
    db_path = Path("gym_manager.db")
    if db_path.exists():
        print("Database found")
        pass
    else:
        print("Database not found/ Database non existent")
        subprocess.run(["python3", "models/db.setup.py"])

    app = QApplication(sys.argv)
    window = GymManager()
    window.show()

    sys.exit(app.exec())