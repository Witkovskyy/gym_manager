import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from ui.main_window import GymManager


def loadStyling(app, stylepath):
    with open(stylepath, "r") as f:
        style = f.read()
        app.setStyleSheet(style)
            
if __name__ == "__main__":
    db_path = Path("gym_manager.db")
    if db_path.exists():
        print("Database found.")
        pass
    else:
        print("Database not found/ Database non existent.")

        n = input("Do you want to create a new database scheme? Y/N.")
        match n:
            case 'Y' | 'y' | "Yes" | "YES" | "yes":
                try:
                    subprocess.run(["python3", "models/db.setup.py"])
                    print("Database successfully created.")
                except:
                    print("Error. Couldn't create database.")
            case _:
                print("Program aborted.")
                sys.exit()

    app = QApplication(sys.argv)
    stylepath = "ui/globalstyle.qss"
    try:
        loadStyling(app, stylepath)
    except FileNotFoundError:
        print(f"Warning: {stylepath} not found. Using default style.")

    window = GymManager()
    window.show()

    sys.exit(app.exec())