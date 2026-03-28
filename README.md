# 🏍️ Motorbike Maintenance Tracker

A lightweight local web application built with **Flask (Python)** to manage motorbike maintenance records, including service history, mileage tracking, and upcoming maintenance alerts.

🔗 Live Demo: https://lulucodes2.pythonanywhere.com/

---

## 📌 Project Overview

This project was developed as part of the **COMP8066 – AI-Powered Software Development** module.

The aim was to design and implement a **small but complete SDLC project**, demonstrating:
- End-to-end development (requirements → deployment)
- Intentional use of **AI tools**
- Critical evaluation of AI-generated outputs
- Clean MVP delivery with testing and documentation

---

## 🚀 Features

### Core Features (MVP)
- Add, edit, and delete motorbikes
- Add, edit, and delete maintenance records
- Store:
  - Service date
  - Mileage
  - Cost
  - Notes
  - Maintenance type
- View maintenance history
- Filter records by bike or maintenance type

### 🔧 Advanced Feature
- **Maintenance Due Engine**
  - Identifies:
    - ✅ OK
    - ⚠️ Due Soon
    - ❌ Overdue
  - Based on mileage and/or service date logic

---

## 🧱 Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Python (Flask) |
| Frontend | HTML, CSS, JavaScript |
| Templates | Jinja2 |
| Database | SQLite (local storage) |
| Testing | pytest |
| Deployment | PythonAnywhere |

---

## 📂 Project Structure

Motorbike-Maintenance-Tracker/
│
├── app.py                 # Main Flask application (routes/controllers)
├── models.py              # Database models (SQLAlchemy)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
│
├── instance/
│   └── maintenance.db     # SQLite database
│
├── templates/             # HTML templates (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── bikes.html
│   ├── records.html
│   └── …
│
├── static/
│   ├── style.css
│   └── app.js
│
├── tests/
│   └── test_app.py        # Unit + integration tests
│
└── docs/                  # Coursework documentation

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/LuluLogics/Motorbike-Maintenance-Tracker.git
cd Motorbike-Maintenance-Tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```


### 5. Open in browser

```bash
http://127.0.0.1:5000/
```


## 🧪 Testing

Run tests using:

```bash
pytest
```

Test Coverage Includes:
	•	Maintenance due logic
	•	Record creation and validation
	•	CRUD operations
	•	Integration flow:
	•	Create → Save → Reload














