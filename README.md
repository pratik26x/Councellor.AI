# Counsellor.AI

> India's complete student counselling platform — college predictions, scholarships, study materials, PG accommodation, mess & tiffin finder, and user authentication.

---

## Quick Start — Single Command

Open a terminal in the project root folder and run these **3 commands**:

```bash
pip install -r requirements.txt
cd backend
python main.py
```

Then open your browser at:
```
http://127.0.0.1:5000
```

> Works in **VS Code**, **PyCharm**, **Sublime Text**, **Cursor**, **Kiro**, **CMD**, **PowerShell**, **Git Bash**, **Terminal (Mac/Linux)** — any environment with Python 3.8+.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Project Structure](#2-project-structure)
3. [Installation — Step by Step](#3-installation--step-by-step)
4. [Running the Project](#4-running-the-project)
5. [IDE-Specific Instructions](#5-ide-specific-instructions)
6. [First-Time Setup](#6-first-time-setup)
7. [Pages & URLs](#7-pages--urls)
8. [API Reference](#8-api-reference)
9. [Database](#9-database)
10. [Switching to MySQL](#10-switching-to-mysql-optional)
11. [Troubleshooting](#11-troubleshooting)
12. [Tech Stack & Dependencies](#12-tech-stack--dependencies)

---

## 1. Prerequisites

### Python 3.8 or higher (required)

Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

> **Windows:** During installation tick **"Add Python to PATH"** — this is critical.

Verify:
```bash
python --version
# Expected: Python 3.8.x or higher
```

### pip (comes with Python 3.4+)
```bash
pip --version
# Expected: pip 22.x or higher
```

If pip is outdated, upgrade it:
```bash
python -m pip install --upgrade pip
```

---

## 2. Project Structure

```
councellor 1/
│
├── backend/                        ← Python / Flask backend
│   ├── main.py                     ← Unified Flask server (port 5000)
│   ├── predict.py                  ← MHT-CET prediction logic
│   ├── pharmacy.py                 ← Pharmacy prediction logic
│   ├── bits.py                     ← BITSAT prediction logic
│   ├── details.py                  ← Student profile (legacy)
│   ├── counsellor.db               ← SQLite DB (auto-created on first run)
│   └── data/                       ← CSV data files (read-only)
│       ├── college_cutoffs.csv
│       ├── pharmacy_colleges_cutoffs.csv
│       ├── BITSAT_Cutoffs.csv
│       ├── iit-and-nit-colleges-admission-criteria-version-2.csv
│       └── ...
│
├── frontend/
│   ├── pages/                      ← All HTML pages
│   │   ├── index.html              ← Homepage
│   │   ├── login.html              ← Login & Register
│   │   ├── profile.html            ← User profile & settings
│   │   ├── details.html            ← Student details form
│   │   ├── dashboard.html          ← Exam predictor dashboard
│   │   ├── predict.html            ← MHT-CET predictor
│   │   ├── pharmacy.html           ← Pharmacy predictor
│   │   ├── bits.html               ← BITSAT predictor
│   │   ├── jee.html                ← JEE predictor
│   │   ├── scholarships.html       ← Scholarships finder
│   │   ├── resources.html          ← PYQs & Study Materials
│   │   ├── accommodation.html      ← PG & Flat finder
│   │   ├── mess.html               ← Mess & Tiffin finder
│   │   └── er-diagram.html         ← Database ER diagram
│   │
│   ├── css/                        ← All stylesheets
│   ├── js/                         ← All JavaScript files
│   └── assets/                     ← Images and static files
│
├── requirements.txt                ← All Python dependencies (pinned versions)
├── run.bat                         ← Windows one-click launcher
└── README.md                       ← This file
```

---

## 3. Installation — Step by Step

### Step 1 — Navigate to the project folder

```bash
# Windows CMD / PowerShell
cd "d:\coding\councellor 1\councellor 1"

# Mac / Linux
cd "/path/to/councellor 1/councellor 1"
```

### Step 2 — Install all dependencies

```bash
pip install -r requirements.txt
```

This installs every required package at the exact tested version. Expected output ends with:
```
Successfully installed flask-3.1.1 flask-cors-4.0.1 flask-sqlalchemy-3.1.1 ...
```

If you get a permissions error on Mac/Linux:
```bash
pip install -r requirements.txt --user
```

Or use a virtual environment (recommended):
```bash
# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3 — Verify all packages installed correctly

```bash
python -c "import flask, flask_cors, flask_sqlalchemy, pandas, werkzeug; print('All OK')"
```

Expected:
```
All OK
```

---

## 4. Running the Project

### The single command (works everywhere)

```bash
cd backend
python main.py
```

### Expected output

```
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

### Open in browser

```
http://127.0.0.1:5000
```

> **Always use the server URL.** Opening HTML files directly (`file://`) will not work — the JavaScript API calls require the Flask server.

### Stop the server

Press `Ctrl + C` in the terminal.

---

## 5. IDE-Specific Instructions

### VS Code

1. Open the project folder: `File → Open Folder → select "councellor 1"`
2. Open the integrated terminal: `` Ctrl + ` ``
3. Run:
   ```bash
   pip install -r requirements.txt
   cd backend
   python main.py
   ```
4. Or use the **Run** button — open `backend/main.py`, press `F5`
   - VS Code may ask to select interpreter — choose Python 3.8+

**Recommended VS Code extensions:**
- Python (Microsoft)
- Pylance

---

### PyCharm

1. Open project: `File → Open → select "councellor 1"` folder
2. Set Python interpreter: `File → Settings → Project → Python Interpreter → Add → Python 3.8+`
3. Install dependencies: Open terminal (`Alt + F12`) and run:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   - Open `backend/main.py`
   - Click the green **Run** button (▶) at the top right
   - Or right-click → `Run 'main'`
5. PyCharm will show the URL in the Run panel — click it or open `http://127.0.0.1:5000`

---

### Cursor / Kiro / Other AI IDEs

1. Open the project folder
2. Open the integrated terminal
3. Run:
   ```bash
   pip install -r requirements.txt
   cd backend
   python main.py
   ```

---

### Windows CMD (Command Prompt)

```cmd
cd /d "d:\coding\councellor 1\councellor 1"
pip install -r requirements.txt
cd backend
python main.py
```

Or just double-click `run.bat` in the project root.

---

### Windows PowerShell

```powershell
Set-Location "d:\coding\councellor 1\councellor 1"
pip install -r requirements.txt
Set-Location backend
python main.py
```

---

### Mac / Linux Terminal

```bash
cd "/path/to/councellor 1/councellor 1"
pip3 install -r requirements.txt
cd backend
python3 main.py
```

> On Mac/Linux use `pip3` and `python3` if `pip` / `python` point to Python 2.

---

### Git Bash (Windows)

```bash
cd "d:/coding/councellor 1/councellor 1"
pip install -r requirements.txt
cd backend
python main.py
```

---

## 6. First-Time Setup

On the **very first run**, the server automatically:

1. Creates `backend/counsellor.db` (SQLite database)
2. Creates all 7 database tables
3. Seeds demo data:
   - **15 scholarships** (Merit, SC/ST, OBC, EWS, Girls, Sports, Minority)
   - **29 study resources** (PYQs, Notes, Formula Sheets, Videos, Mock Tests)
   - **18 accommodation listings** (PGs, Flats, Hostels across Maharashtra)
   - **18 mess & tiffin services** (across Maharashtra)

No manual database setup needed.

### Create your first account

1. Go to `http://127.0.0.1:5000/pages/login.html`
2. Click **"Create Account"** tab
3. Fill in name, email, username, password (min. 6 characters)
4. Click **"Create Account"** — logged in automatically and redirected to homepage

---

## 7. Pages & URLs

| Page | URL |
|---|---|
| Homepage | `http://127.0.0.1:5000` |
| Login / Register | `http://127.0.0.1:5000/pages/login.html` |
| My Profile | `http://127.0.0.1:5000/pages/profile.html` |
| Student Details | `http://127.0.0.1:5000/pages/details.html` |
| Exam Dashboard | `http://127.0.0.1:5000/pages/dashboard.html` |
| MHT-CET Predictor | `http://127.0.0.1:5000/pages/predict.html` |
| Pharmacy Predictor | `http://127.0.0.1:5000/pages/pharmacy.html` |
| BITSAT Predictor | `http://127.0.0.1:5000/pages/bits.html` |
| JEE Predictor | `http://127.0.0.1:5000/pages/jee.html` |
| Scholarships | `http://127.0.0.1:5000/pages/scholarships.html` |
| Study Materials | `http://127.0.0.1:5000/pages/resources.html` |
| Accommodation | `http://127.0.0.1:5000/pages/accommodation.html` |
| Mess & Tiffin | `http://127.0.0.1:5000/pages/mess.html` |
| ER Diagram | `http://127.0.0.1:5000/pages/er-diagram.html` |

---

## 8. API Reference

Base URL: `http://127.0.0.1:5000`

### Auth endpoints

```
POST  /api/auth/register          Body: {full_name, email, username, password}
POST  /api/auth/login             Body: {identifier, password}
POST  /api/auth/logout            Header: Authorization: Bearer <token>
GET   /api/auth/me                Header: Authorization: Bearer <token>
PUT   /api/auth/update            Body: {full_name, username}
PUT   /api/auth/change-password   Body: {current_password, new_password}
DELETE /api/auth/delete           Header: Authorization: Bearer <token>
```

### Predictor endpoints

```
POST  /api/predict/mhtcet    Body: {percentile, category, branch?, preferred_cities?}
POST  /api/predict/pharmacy  Body: {percentile, category, branch?, preferred_cities?}
POST  /api/predict/bitsat    Body: {score, campus?}
POST  /api/predict/jee       Body: {rank, category, gender, branch?, preferred_cities?}
```

### Data endpoints

```
GET   /api/scholarships              Query: category=, search=
POST  /api/scholarships              Body: scholarship object
GET   /api/resources                 Query: exam=, subject=, type=, year=, search=
POST  /api/resources/<id>/download
GET   /api/accommodation             Query: city=, type=, gender=, max_rent=
POST  /api/accommodation             Body: listing object
GET   /api/mess                      Query: city=, type=, max_cost=
POST  /api/mess                      Body: service object
POST  /api/student                   Body: student profile object
```

---

## 9. Database

- **Engine:** SQLite (file-based, no server needed)
- **File:** `backend/counsellor.db`
- **Auto-created:** Yes, on first run

### View the database

**DB Browser for SQLite** (free, recommended):
1. Download: [https://sqlitebrowser.org/dl/](https://sqlitebrowser.org/dl/)
2. Open `backend/counsellor.db`

### Reset the database

```bash
# Windows
del "d:\coding\councellor 1\councellor 1\backend\counsellor.db"
cd backend
python main.py

# Mac / Linux
rm "/path/to/backend/counsellor.db"
cd backend
python3 main.py
```

---

## 10. Switching to MySQL (Optional)

```bash
pip install pymysql
```

In `backend/main.py`, change:
```python
# From (SQLite):
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE, 'counsellor.db')

# To (MySQL):
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/counsellor_ai'
```

Create the database in MySQL first:
```sql
CREATE DATABASE counsellor_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then restart: `python main.py` — tables are created automatically.

---

## 11. Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| `python: command not found` | Install Python and add to PATH |
| `Address already in use` (port 5000) | Kill the process: `netstat -ano \| findstr :5000` then `taskkill /PID <id> /F` |
| Page shows blank / API not working | Make sure server is running at `http://127.0.0.1:5000` |
| `No such file or directory: 'college_cutoffs.csv'` | Run `python main.py` from inside the `backend/` folder |
| Login button not working | Clear browser localStorage: F12 → Application → Local Storage → Clear |
| No prediction results | Try lower percentile / higher rank, remove city filter |
| Database errors after model changes | Delete `counsellor.db` and restart server |

---

## 12. Tech Stack & Dependencies

### Python packages (all in requirements.txt)

| Package | Version | Why it's needed |
|---|---|---|
| `flask` | 3.1.1 | Web framework — routes, request handling, static files |
| `werkzeug` | 3.1.3 | Password hashing (PBKDF2-SHA256), WSGI utilities |
| `jinja2` | 3.1.6 | Flask's templating engine (used internally) |
| `markupsafe` | 3.0.2 | Safe HTML escaping (Jinja2 dependency) |
| `click` | 8.2.1 | Flask CLI commands |
| `itsdangerous` | 2.2.0 | Secure token signing (Flask sessions) |
| `blinker` | 1.9.0 | Flask signals |
| `flask-cors` | 4.0.1 | Allows browser JS to call the API (CORS headers) |
| `flask-sqlalchemy` | 3.1.1 | ORM — Python classes map to database tables |
| `sqlalchemy` | 2.0.49 | Database engine and query builder |
| `greenlet` | 3.5.0 | Async context switching (SQLAlchemy dependency) |
| `pandas` | 2.3.2 | Reads CSV files, filters college cutoff data |
| `numpy` | 2.2.6 | Numerical operations (pandas dependency) |
| `python-dateutil` | 2.9.0.post0 | Date parsing (pandas dependency) |
| `pytz` | 2025.2 | Timezone support (pandas dependency) |
| `tzdata` | 2025.2 | Timezone database (pandas dependency) |
| `six` | 1.17.0 | Python 2/3 compatibility (dateutil dependency) |

### Frontend (no installation needed)

| Technology | Version | Role |
|---|---|---|
| HTML5 | — | Page structure |
| CSS3 | — | Styling (no framework, custom CSS) |
| JavaScript ES6+ | — | Interactivity, fetch API calls |
| Google Fonts | CDN | Space Grotesk, Inter typefaces |

### Database

| Technology | Role |
|---|---|
| SQLite 3 | Default database (built into Python, no install needed) |
| MySQL (optional) | Production-grade alternative |

---

## Final Command Summary

```bash
# ── One-time setup ──────────────────────────────────────────
pip install -r requirements.txt

# ── Every time you want to run the project ──────────────────
cd backend
python main.py

# ── Then open in browser ────────────────────────────────────
# http://127.0.0.1:5000
```

---

*&copy; 2026 Counsellor.AI &mdash; *
