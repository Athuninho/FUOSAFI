# FUOSAFI – COMMUNITY-BASED COASTAL AND MARINE POLLUTION REPORTING SYSTEM

**FUOSAFI** is a full-stack, responsive, community-driven environmental reporting web application built with Python, Streamlit, SQLite, and Folium. It connects coastal community members, local representatives (*Mzee wa Mtaa*), and environmental authorities into an organized, transparent reporting and tracking workflow.

---

## 🌊 Core Features & Modules

### 1. Multi-Role Role-Based Access Control (RBAC)
- **Resident**: Self-registration, personal dashboard, pollution incident creation (title, category, date, area, coordinates, map pin, photo upload), tamper-evident reference number generation, incident progress tracking, and audit trail inspection.
- **Mzee wa Mtaa (Community Representative)**: Administrative review queue, report completeness checks, site inspection remark logging, status updates, and institutional referrals to environmental bodies.
- **Authority Representative (Demonstration Interface)**: Dedicated institutional interface to view referred reports, acknowledge referrals, log official intervention actions, and record resolutions.
- **System Administrator**: Centralized oversight, registered user management (role assignments, deactivation), system-wide analytics, and audit logging.

### 2. Pollution Categories Supported
1. **Coastal and marine litter** (e.g. marine debris, microplastics, discarded fishing nets).
2. **Improperly dumped solid garbage** (e.g. municipal/commercial waste in mangrove or coastal areas).
3. **Sewage and wastewater entering coastal or marine environments** (e.g. outfall pipes, drain overflows).

### 3. Geographical Mapping & GIS Module
- Integrated **Folium & Streamlit-Folium** interactive maps.
- Real-time clickable map coordinate selection for incident pinning.
- Dynamic clustering and color-coded status pins for incident visualization across coastal counties (Mombasa, Kwale, Kilifi, Lamu, Tana River).

### 4. End-to-End Status Lifecycle & Audit Trail
Every status transition is logged in the `report_history` table with previous state, new state, responsible actor, and timestamp:
`Submitted` ➔ `Under Community Review` ➔ `Awaiting Additional Information` ➔ `Referred to Authority` ➔ `Acknowledged by Authority` ➔ `In Progress` ➔ `Resolved (Recorded)` ➔ `Closed`.

---

## 🛠️ Technology Stack

- **Backend / Web Framework**: Python 3.14, Streamlit
- **Database**: SQLite3 (`fuosafi.db` with enforced `PRAGMA foreign_keys = ON` and WAL mode)
- **Data Analytics & Visualization**: Pandas, Streamlit native charts
- **GIS / Mapping**: Folium, Streamlit-Folium
- **Image Processing & Safety**: Pillow (PIL)
- **Security**: Bcrypt password hashing, parameterised queries, input sanitization
- **Automated Testing**: Pytest

---

## 📁 Project Structure

```
FUOSAFI/
├── app.py                              # Application entry point & role router
├── config.py                           # App configuration, constants & styles
├── requirements.txt                    # Project dependencies
├── pytest.ini                          # Pytest configuration
├── README.md                           # Documentation
├── .gitignore                          # Git ignore rules
│
├── assets/
│   └── css/
│       └── style.css                   # Coastal-inspired styling & cards
│
├── database/
│   ├── db.py                           # SQLite connection manager & query helpers
│   ├── schema.sql                      # Relational database schema with foreign keys
│   └── init_db.py                      # Database initialization & demonstration seed script
│
├── modules/
│   ├── auth/
│   │   ├── authentication.py           # Bcrypt verification & registration logic
│   │   ├── login.py                    # Login form UI & session handling
│   │   └── register.py                 # Resident registration UI
│   │
│   ├── reports/
│   │   ├── create_report.py            # Observation submission form & map picker
│   │   ├── view_reports.py             # Incident listing, inspection & photo display
│   │   └── tracking.py                 # Report lifecycle service & audit logger
│   │
│   ├── community/
│   │   └── review.py                   # Mzee wa Mtaa review & referral workflow
│   │
│   ├── authority/
│   │   └── responses.py                # Authority response & referral acknowledgement
│   │
│   └── analytics/
│       └── dashboard.py                # Pandas KPI metrics & system charts
│
├── pages/
│   ├── resident.py                     # Resident dashboard & workspace
│   ├── community_representative.py     # Community Representative portal
│   ├── authority.py                    # Authority Representative portal
│   └── admin.py                        # Administrator oversight portal
│
├── utils/
│   ├── security.py                     # Bcrypt hashing & password validation
│   ├── reference_generator.py          # Unique reference code generator (FUO-YYYYMMDD-XXXX)
│   ├── validators.py                   # Image & coordinate boundary validators
│   ├── helpers.py                      # Formatting & status badge generators
│   └── map_builder.py                  # Folium map builder & coordinate picker
│
├── data/
│   └── uploads/                        # Secure image upload storage
│
└── tests/
    ├── test_auth.py                    # 6 unit tests for registration & authentication
    ├── test_database.py                # 4 integration tests for schema & foreign keys
    └── test_reports.py                 # 2 end-to-end tests for reporting & referral lifecycle
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Git (optional)

### Option A: One-Click Launcher (Easiest on Windows)
Simply double-click the included `run_app.bat` script, or run:
```powershell
.\run_app.bat
```

### Option B: Run Directly via Virtual Environment Python (No Script Activation Needed)
On Windows PowerShell where script execution policy is restricted, you do not need to activate `Activate.ps1`. Run directly using the virtual environment's Python binary:
```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

### Option C: If You Prefer Activating the Environment in PowerShell
If you want standard environment activation, allow scripts for the current terminal session first:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🔑 Pre-Configured Demonstration Accounts

| Role | Email | Password |
| :--- | :--- | :--- |
| **Resident** | `resident@fuosafi.org` | `ResidentPass123` |
| **Mzee wa Mtaa (Community Rep)** | `mzee@fuosafi.org` | `MzeePass123` |
| **Authority Representative (NEMA)** | `authority@fuosafi.org` | `AuthorityPass123` |
| **Administrator** | `admin@fuosafi.org` | `AdminPass123` |

*New residents can also register directly via the **Register Resident Account** tab.*

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:
```powershell
.\venv\Scripts\pytest -v
```
All **12 automated tests** across authentication, database integrity, and workflow lifecycle execute and pass.
