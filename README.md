# 🛠️ GearGuard - The Ultimate Maintenance Tracker

<div align="center">

![GearGuard Logo](https://img.shields.io/badge/GearGuard-Maintenance%20Tracker-blue?style=for-the-badge&logo=tools)

![License](https://img.shields.io/badge/License-LGPL--3-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![Hackathon](https://img.shields.io/badge/Odoo-Hackathon%202025-orange?logo=odoo)
![Status](https://img.shields.io/badge/Status-Active-success)

**A comprehensive maintenance management system for tracking company assets, managing maintenance requests, and coordinating service teams.**

[Features](#-features) • [Installation](#-installation) • [API Reference](#-api-reference) • [Screenshots](#-screenshots) • [Team](#-team)

</div>

---

## 👨‍💻 Team QuantCoder

| Role | Name | College |
|:----:|:----:|:-------:|
| 👑 **Team Leader** | Gabani Abhi Dineshbhai | GCET |
| 👨‍💻 **Team Member** | Tirth Goyani | GCET |

> 🎓 **College**: G H Patel College of Engineering & Technology (GCET), Vallabh Vidyanagar

---

## 🎯 Project Overview

GearGuard is a full-stack maintenance management application built with **Flask** (Python) backend and modern JavaScript frontend. It enables organizations to:

- 📦 **Track Equipment/Assets** - Maintain a centralized database of all company assets
- 🔧 **Manage Maintenance Requests** - Handle corrective and preventive maintenance workflows
- 👥 **Coordinate Teams** - Assign work to specialized maintenance teams and technicians
- 📊 **Analyze Performance** - View reports, dashboards, and maintenance history
- 📅 **Schedule Maintenance** - Calendar-based planning for preventive maintenance

---

## ✨ Features

### 🏠 Dashboard
- **Real-time Statistics** - Equipment status, open requests, overdue items
- **Interactive Charts** - Requests by stage, priority distribution, monthly trends
- **Recent Activity** - Latest maintenance requests at a glance
- **Quick Actions** - Fast access to common operations

### 📦 Equipment Management
| Feature | Description |
|---------|-------------|
| Central Asset Database | Track all company assets with detailed information |
| Auto-Generated Codes | Sequential equipment codes (EQ-0001, EQ-0002...) |
| Warranty Tracking | Monitor warranty status with expiration alerts |
| Status Management | Operational, Maintenance, Broken, Scrapped states |
| Default Assignments | Pre-configure default team and technician |
| Maintenance History | View all maintenance records per equipment |

### 🔧 Maintenance Requests
| Feature | Description |
|---------|-------------|
| **Corrective Requests** 🔴 | Unplanned repairs for equipment breakdowns |
| **Preventive Requests** 🔵 | Scheduled routine maintenance and checkups |
| Priority Levels | Low, Normal, High, Urgent with visual indicators |
| Kanban Board | Drag-and-drop workflow management |
| Auto-Fill Logic | Auto-populate team/category from equipment |
| Overdue Detection | Visual alerts for past-deadline requests |
| Stage Workflow | New → In Progress → Repaired → Scrap |

### 👥 Team Management
- Create specialized teams (Mechanics, Electricians, IT Support)
- Assign team members and leaders
- Track team workload and performance
- Color-coded team identification

### 👷 Technician Management
- Individual technician profiles
- Skill type tracking (Mechanical, Electrical, HVAC, IT, General)
- Availability status (Available, Busy, On Leave, Training)
- Hourly rate management
- Certification tracking

### 📅 Calendar View
- Scheduled maintenance visualization
- Color-coded by team
- Drag-and-drop rescheduling
- Monthly/weekly/daily views

### 📊 Reports & Analytics
- **Summary Reports** - Overview of all maintenance metrics
- **Equipment Breakdown** - Analysis by category and status
- **Team Performance** - Request completion rates
- **Trend Analysis** - Historical data visualization

### 🔐 User Authentication & Authorization
| Role | Permissions |
|------|-------------|
| **Admin** | Full system access - manage users, settings, all features |
| **Manager** | Manage teams, equipment, requests, view reports |
| **Technician** | Complete assigned requests, update status |
| **User** | Create requests, view equipment (read-only) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (HTML/JS/CSS)                 │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│   │Dashboard │  │Equipment │  │Requests  │  │ Calendar │    │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Flask Backend (Python)                    │
│   ┌──────────────────────────────────────────────────────┐  │
│   │                    REST API Layer                    │  │
│   │  /api/equipment  /api/requests  /api/teams  /api/... │  │
│   └──────────────────────────────────────────────────────┘  │
│   ┌──────────────────────────────────────────────────────┐  │
│   │                Authentication Layer                  │  │
│   │  Session-based  |  Role-Based Access Control (RBAC)  │  │
│   └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLAlchemy ORM                           │
│   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐  │
│   │  User  │ │Equipmt │ │Request │ │  Team  │ │Technician│  │
│   └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              SQLite (Dev) / PostgreSQL (Prod)               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
odoo-hackathon/
├── 📄 app.py                      # Main application entry point
├── 📄 requirements.txt            # Python dependencies
├── 📄 README.md                   # This file
├── 📄 API_TEST_GUIDE.md           # API testing documentation
│
├── 📂 backend/                    # Backend application
│   ├── __init__.py
│   ├── config.py                  # Configuration settings
│   ├── seed.py                    # Database seeding script
│   │
│   ├── 📂 models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py                # User & Role models
│   │   ├── equipment.py           # Equipment model
│   │   ├── equipment_category.py  # Equipment categories
│   │   ├── maintenance_request.py # Maintenance requests
│   │   ├── maintenance_stage.py   # Request stages
│   │   ├── maintenance_team.py    # Maintenance teams
│   │   └── technician.py          # Technician profiles
│   │
│   └── 📂 routes/                 # API & View routes
│       ├── __init__.py
│       ├── api.py                 # REST API endpoints (1300+ lines)
│       ├── auth.py                # Authentication routes
│       └── views.py               # Page rendering routes
│
├── 📂 frontend/                   # Frontend assets
│   ├── 📂 static/
│   │   ├── 📂 css/
│   │   │   └── style.css          # Custom styles
│   │   └── 📂 js/
│   │       ├── api.js             # API helper functions
│   │       ├── app.js             # Main application JS
│   │       ├── equipment.js       # Equipment module
│   │       └── requests.js        # Requests module
│   │
│   └── 📂 templates/              # Jinja2 templates
│       ├── base.html              # Base template
│       ├── dashboard.html         # Main dashboard
│       ├── calendar.html          # Calendar view
│       ├── categories.html        # Categories management
│       ├── teams.html             # Teams management
│       ├── technicians.html       # Technicians page
│       ├── reports.html           # Reports & analytics
│       ├── history.html           # Maintenance history
│       ├── settings.html          # System settings
│       ├── management.html        # Management page
│       ├── workcenters.html       # Work centers
│       ├── profile.html           # User profile
│       │
│       ├── 📂 auth/
│       │   ├── login.html         # Login page
│       │   └── signup.html        # Registration page
│       │
│       ├── 📂 equipment/
│       │   ├── list.html          # Equipment list
│       │   └── detail.html        # Equipment details
│       │
│       ├── 📂 requests/
│       │   ├── list.html          # Request list
│       │   └── detail.html        # Request details
│       │
│       └── 📂 partials/
│           └── sidebar.html       # Navigation sidebar
│
├── 📂 gearguard/                  # Odoo module (optional)
│   └── __manifest__.py
│
├── 📂 instance/                   # Instance folder (database)
│
└── 📂 tests/                      # Test files
    ├── test_api_like_user.py      # User simulation tests
    ├── comprehensive_backend_test.py
    └── test_backend.sh            # Shell test script
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/ADG1411/odoo-hackathon.git
cd odoo-hackathon

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py
```

### Access the Application
Open your browser and navigate to: **http://localhost:5000**

### Default Login Credentials

| Role | Email | Password |
|------|-------|----------|
| 👑 Admin | `admin@gearguard.com` | `admin123` |
| 📋 Manager | `abhi.gabani@gearguard.com` | `password123` |
| 👤 User | `user@gearguard.com` | `user123` |

---

## 📚 API Reference

### Base URL
```
http://localhost:5000
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|:------:|----------|-------------|:-------------:|
| `POST` | `/auth/register` | Register new user | ✅ |
| `POST` | `/auth/login` | User login | ✅ |
| `POST` | `/auth/logout` | User logout | ✅ |
| `GET` | `/auth/me` | Get current user | ✅ |
| `PUT` | `/auth/profile` | Update profile | ✅ |
| `PUT` | `/auth/change-password` | Change password | ✅ |

### Dashboard Endpoints

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/api/dashboard/stats` | Get dashboard statistics |
| `GET` | `/api/dashboard/recent-requests` | Get 10 recent requests |
| `GET` | `/api/dashboard/requests-by-stage` | Requests grouped by stage |
| `GET` | `/api/dashboard/requests-by-priority` | Requests grouped by priority |
| `GET` | `/api/dashboard/equipment-by-status` | Equipment status breakdown |
| `GET` | `/api/dashboard/monthly-requests` | Monthly request trends (6 months) |

### Equipment Endpoints

| Method | Endpoint | Description | Permission |
|:------:|----------|-------------|:----------:|
| `GET` | `/api/equipment` | List all equipment | 🌐 Public |
| `GET` | `/api/equipment/<id>` | Get equipment details | 🌐 Public |
| `POST` | `/api/equipment` | Create equipment | 🔒 Manager+ |
| `PUT` | `/api/equipment/<id>` | Update equipment | 🔒 Manager+ |
| `DELETE` | `/api/equipment/<id>` | Delete equipment | 🔒 Manager+ |
| `GET` | `/api/equipment/<id>/autofill` | Get autofill data | 🌐 Public |
| `POST` | `/api/equipment/<id>/scrap` | Mark equipment as scrapped | 🔒 Manager+ |

**Query Parameters for GET /api/equipment:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `category_id` | int | Filter by category |
| `status` | string | Filter by status (operational, maintenance, broken, scrapped) |
| `search` | string | Search by name or code |
| `page` | int | Page number (default: 1) |
| `per_page` | int | Items per page (default: 20) |

### Category Endpoints

| Method | Endpoint | Description | Permission |
|:------:|----------|-------------|:----------:|
| `GET` | `/api/categories` | List categories | 🌐 Public |
| `GET` | `/api/categories/<id>` | Get category | 🌐 Public |
| `POST` | `/api/categories` | Create category | 🔒 Manager+ |
| `PUT` | `/api/categories/<id>` | Update category | 🔒 Manager+ |
| `DELETE` | `/api/categories/<id>` | Delete category | 🔒 Manager+ |

### Maintenance Request Endpoints

| Method | Endpoint | Description | Permission |
|:------:|----------|-------------|:----------:|
| `GET` | `/api/requests` | List requests | 🌐 Public |
| `GET` | `/api/requests/<id>` | Get request details | 🌐 Public |
| `POST` | `/api/requests` | Create request | 🔒 Login |
| `PUT` | `/api/requests/<id>` | Update request | 🔒 Manager+ |
| `DELETE` | `/api/requests/<id>` | Delete request | 🔒 Manager+ |
| `POST` | `/api/requests/<id>/move-stage` | Change request stage | 🔒 Manager+ |
| `GET` | `/api/requests/kanban` | Get kanban board data | 🌐 Public |

**Query Parameters for GET /api/requests:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `stage_id` | int | Filter by stage |
| `team_id` | int | Filter by team |
| `equipment_id` | int | Filter by equipment |
| `priority` | string | Filter by priority |
| `request_type` | string | Filter by type (corrective, preventive) |
| `overdue` | boolean | Filter overdue requests |

### Stage Endpoints

| Method | Endpoint | Description | Permission |
|:------:|----------|-------------|:----------:|
| `GET` | `/api/stages` | List all stages | 🌐 Public |
| `GET` | `/api/stages/<id>` | Get stage details | 🌐 Public |
| `POST` | `/api/stages` | Create stage | 🔒 Admin |
| `PUT` | `/api/stages/<id>` | Update stage | 🔒 Admin |
| `DELETE` | `/api/stages/<id>` | Delete stage | 🔒 Admin |

### Team Endpoints

| Method | Endpoint | Description | Permission |
|:------:|----------|-------------|:----------:|
| `GET` | `/api/teams` | List teams | 🌐 Public |
| `GET` | `/api/teams/<id>` | Get team details | 🌐 Public |
| `POST` | `/api/teams` | Create team | 🔒 Manager+ |
| `PUT` | `/api/teams/<id>` | Update team | 🔒 Manager+ |
| `DELETE` | `/api/teams/<id>` | Delete team | 🔒 Manager+ |
| `POST` | `/api/teams/<id>/members` | Add team member | 🔒 Manager+ |
| `DELETE` | `/api/teams/<id>/members/<user_id>` | Remove member | 🔒 Manager+ |

### Technician Endpoints

| Method | Endpoint | Description | Permission |
|:------:|----------|-------------|:----------:|
| `GET` | `/api/technicians` | List technicians | 🌐 Public |
| `GET` | `/api/technicians/<id>` | Get technician | 🌐 Public |
| `POST` | `/api/technicians` | Create technician | 🔒 Manager+ |
| `PUT` | `/api/technicians/<id>` | Update technician | 🔒 Manager+ |
| `DELETE` | `/api/technicians/<id>` | Delete technician | 🔒 Manager+ |

**Technician Skill Types:**
- `mechanical` - Mechanical skills
- `electrical` - Electrical skills
- `hvac` - HVAC systems
- `plumbing` - Plumbing
- `it` - IT/Computer systems
- `general` - General maintenance

**Availability Statuses:**
- `available` - Ready for assignments
- `busy` - Currently working
- `on_leave` - On vacation/leave
- `training` - In training

### Report Endpoints

| Method | Endpoint | Description | Permission |
|:------:|----------|-------------|:----------:|
| `GET` | `/api/reports/summary` | Get summary report | 🔒 Manager+ |
| `GET` | `/api/reports/equipment-breakdown` | Equipment analysis | 🔒 Manager+ |
| `GET` | `/api/reports/team-performance` | Team metrics | 🔒 Manager+ |
| `GET` | `/api/reports/maintenance-history` | Historical data | 🔒 Manager+ |

### Calendar Endpoints

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET` | `/api/calendar/events` | Get calendar events |

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | ISO date | Start date range |
| `end` | ISO date | End date range |
| `team_id` | int | Filter by team |

### User Management Endpoints (Admin Only)

| Method | Endpoint | Description | Permission |
|:------:|----------|-------------|:----------:|
| `GET` | `/api/users` | List all users | 🔒 Admin |
| `GET` | `/api/users/<id>` | Get user details | 🔒 Admin |
| `PUT` | `/api/users/<id>` | Update user | 🔒 Admin |
| `DELETE` | `/api/users/<id>` | Delete user | 🔒 Admin |
| `PUT` | `/api/users/<id>/role` | Change user role | 🔒 Admin |
| `GET` | `/api/roles` | List all roles | 🔒 Admin |

---

## 🔄 Workflow Examples

### Corrective Maintenance (Breakdown)
```
1. Equipment breaks down
       ↓
2. User creates request → Type: Corrective
       ↓
3. System auto-fills team based on equipment
       ↓
4. Manager assigns technician
       ↓
5. Technician marks "In Progress"
       ↓
6. Technician completes repair
       ↓
7. Request moved to "Repaired"
```

### Preventive Maintenance (Scheduled)
```
1. Manager creates request → Type: Preventive
       ↓
2. Set scheduled date for maintenance
       ↓
3. Request appears on calendar
       ↓
4. Reminder sent to technician
       ↓
5. Maintenance performed on schedule
       ↓
6. Request completed and logged
```

### Scrap Workflow
```
1. Equipment deemed unrepairable
       ↓
2. Move request to "Scrap" stage
       ↓
3. System automatically:
   - Marks equipment as scrapped
   - Records scrap date
   - Logs scrap reason
```

---

## 🧪 Testing

### Run API Tests
```bash
# Make sure the server is running first
python app.py

# In another terminal, run tests
python test_api_like_user.py
```

### Test Scenarios Covered

**Scenario 1: Admin User Workflow (11 tests)**
- ✅ Login as admin
- ✅ View dashboard statistics
- ✅ View requests by stage chart
- ✅ List all equipment
- ✅ View equipment details
- ✅ Test autofill functionality
- ✅ List maintenance teams
- ✅ View calendar events
- ✅ Generate reports summary
- ✅ View equipment breakdown
- ✅ Logout

**Scenario 2: Manager User Workflow (10 tests)**
- ✅ Login as manager
- ✅ Create new equipment
- ✅ Create maintenance request
- ✅ Update request (change priority)
- ✅ Move request to different stage (Kanban)
- ✅ View all requests
- ✅ Filter requests by priority
- ✅ Filter requests by type
- ✅ Logout

**Scenario 3: Regular User Workflow (3 tests)**
- ✅ Login as user
- ✅ View equipment (read-only)
- ✅ View requests (read-only)
- ✅ Logout

### Comprehensive Backend Tests
```bash
python comprehensive_backend_test.py
```

### Shell Test Script
```bash
chmod +x test_backend.sh
./test_backend.sh
```

---

## 🛠️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `gearguard-secret-key-2024` | Flask secret key for sessions |
| `DATABASE_URL` | `sqlite:///gearguard.db` | Database connection string |
| `FLASK_ENV` | `development` | Environment mode |

### Database Configuration

**Development (SQLite):**
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///gearguard.db'
```

**Production (PostgreSQL):**
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/gearguard'
```

### Application Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `APP_NAME` | `GearGuard` | Application name |
| `APP_VERSION` | `1.0.0` | Current version |
| `ITEMS_PER_PAGE` | `20` | Default pagination size |
| `SESSION_TYPE` | `filesystem` | Session storage type |
| `PERMANENT_SESSION_LIFETIME` | `7 days` | Session duration |

---

## 📋 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | Database ORM |
| psycopg2-binary | 2.9.9 | PostgreSQL adapter |
| python-dateutil | 2.8.2 | Date utilities |
| gunicorn | 21.2.0 | Production WSGI server |
| requests | 2.31.0 | HTTP library for testing |

---

## 🤖 Smart Features

### Auto-Fill Logic
When creating a maintenance request:
1. Select equipment
2. **Category** auto-populates from equipment
3. **Default Team** auto-assigned based on equipment configuration
4. **Default Technician** can be pre-assigned

```json
// GET /api/equipment/1/autofill
{
  "category_id": 1,
  "category_name": "Machinery",
  "team_id": 2,
  "team_name": "Mechanics",
  "technician_id": 5,
  "technician_name": "John Smith"
}
```

### Scrap Logic
When moving a request to "Scrap" stage:
- ✅ Equipment automatically marked as scrapped
- ✅ Scrap date recorded
- ✅ Scrap reason logged from request

### Smart Buttons
- Equipment form shows maintenance count badge
- Quick access to filtered request list
- Visual indicators for overdue status

### Overdue Detection
- Automatic calculation based on deadline
- Visual alerts in UI
- Filter endpoint for overdue requests
- Dashboard statistics

---

## 🎨 UI Features

| Feature | Technology |
|---------|------------|
| Responsive Design | Bootstrap 5 |
| Icons | Bootstrap Icons |
| Charts | Chart.js |
| Calendar | FullCalendar |
| Date Picker | Flatpickr |
| Notifications | Toast messages |
| Modals | Bootstrap Modal |
| Tables | DataTables |

---

## 📊 Database Schema

### Core Entities

```
┌─────────────────┐       ┌─────────────────┐
│      User       │       │      Role       │
├─────────────────┤       ├─────────────────┤
│ id              │──────<│ id              │
│ email           │       │ name            │
│ first_name      │       │ description     │
│ last_name       │       │ can_manage_*    │
│ role_id         │       └─────────────────┘
│ is_active       │
└─────────────────┘
         │
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│    Equipment    │──────<│EquipmentCategory│
├─────────────────┤       ├─────────────────┤
│ id              │       │ id              │
│ code            │       │ name            │
│ name            │       │ color           │
│ category_id     │       │ icon            │
│ serial_number   │       └─────────────────┘
│ status          │
│ default_team_id │
└─────────────────┘
         │
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│MaintenanceRequest│─────<│MaintenanceStage │
├─────────────────┤       ├─────────────────┤
│ id              │       │ id              │
│ reference       │       │ name            │
│ name            │       │ sequence        │
│ equipment_id    │       │ color           │
│ team_id         │       │ is_done         │
│ stage_id        │       │ is_scrap        │
│ request_type    │       └─────────────────┘
│ priority        │
│ deadline        │
└─────────────────┘
         │
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│MaintenanceTeam  │──────<│   TeamMember    │
├─────────────────┤       ├─────────────────┤
│ id              │       │ team_id         │
│ name            │       │ user_id         │
│ color           │       │ is_leader       │
│ is_active       │       └─────────────────┘
└─────────────────┘
```

---

## 📝 License

This project is licensed under **LGPL-3.0** - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write unit tests for new features

---

## 🐛 Known Issues & Roadmap

### Current Limitations
- [ ] Email notifications not yet implemented
- [ ] File attachments for requests pending
- [ ] Mobile app version in planning

### Future Enhancements
- [ ] 📧 Push notifications & email alerts
- [ ] 📱 QR code scanning for equipment
- [ ] 🤖 AI-powered predictive maintenance
- [ ] 🌍 Multi-language support (i18n)
- [ ] 🔌 Integration with IoT sensors
- [ ] 📤 Export reports to PDF/Excel
- [ ] 🔗 API rate limiting
- [ ] 📊 Advanced analytics dashboard

---

## 📞 Support

For support, please:
- 📧 Open an issue on [GitHub](https://github.com/ADG1411/odoo-hackathon/issues)
- 💬 Contact the team

---

## 🙏 Acknowledgments

- **Odoo** for the hackathon opportunity
- **Flask** team for the amazing framework
- **Bootstrap** for the UI components
- **GCET** for supporting innovation

---

<div align="center">

## ⭐ Star This Repository!

If you found this project helpful, please consider giving it a star!

[![GitHub stars](https://img.shields.io/github/stars/ADG1411/odoo-hackathon?style=social)](https://github.com/ADG1411/odoo-hackathon)

---

**GearGuard** - Keep your assets running smoothly! 🛠️

Made with ❤️ by **Team QuantCoder** | GCET

*Odoo Hackathon 2025*

---

![Footer](https://img.shields.io/badge/Built%20with-Flask%20%7C%20SQLAlchemy%20%7C%20Bootstrap-blue?style=for-the-badge)

</div>
