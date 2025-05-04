
# 🏋️ Gym Manager — Membership Management System

A desktop application for managing gym memberships and clients, built with **Python**, **PyQt6**, and **SQLAlchemy**.

Built to potentially implement in my workplace.
Entires in databases are randomly generated.
---

## 📦 Features

- Add new gym clients with customizable membership types and durations
- Delete clients from the database with filtering options
- View the list of all clients in a table view
- Automatically calculates membership expiry date
- RODO and underage status tracking
- Comment field for additional notes per client
- Data persistence via SQLite and SQLAlchemy ORM

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/witkovskyy/gym_manager.git
cd gym_manager
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Initialize the database (if not already created)**

Make sure the database schema is set up. You can use Alembic, or ensure `db_setup.py` is run to create tables via SQLAlchemy.

---

## 🧠 Usage

Run the main application:

```bash
python main.py
```

You will see the main window with options to add or delete gym members.

---

## 📁 Project Structure

```
gym_manager/
├── main.py                   # Main entry point
├── models/
│   └── db_setup.py           # SQLAlchemy models and engine
├── views/
│   ├── add_client_popup.py   # Add client dialog
│   └── del_client_popup.py   # Delete client dialog
├── resources/
│   └── (icons, styles, etc.)
├── gym_manager.db            # SQLite database (created on first run)
└── README.md
```

---

## ✅ TODO / Roadmap

- [ ] Edit client information
- [ ] Export data to CSV/PDF
- [ ] Membership history tracking
- [ ] Responsive design improvements

---

## 🛠 Technologies Used

- [PyQt6](https://pypi.org/project/PyQt6/) — GUI Framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for database interaction
- [SQLite](https://www.sqlite.org/index.html) — Embedded database
- [Python 3.9+](https://www.python.org/)

---

## 👤 Author

- **Witkovskyy** — [@witkovskyy](https://github.com/witkovskyy)

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
