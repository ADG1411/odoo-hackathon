# GearGuard: The Ultimate Maintenance Tracker


![License](https://img.shields.io/badge/License-Team-QuantCoder)
![Hackathon](https://img.shields.io/badge/Odoo-Hackathon-orange)

---

## 👨‍💻 Team QuantCoder

| Role | Name | College |
|------|------|---------|
| 👑 **Team Leader** | Gabani Abhi Dineshbhai | GCET |
| 👨‍💻 **Team Member** | Tirth Goyani | GCET |

> 🎓 **College**: G H Patel College of Engineering & Technology (GCET), Vallabh Vidyanagar

---

## 🎯 Overview

GearGuard is a comprehensive Odoo maintenance management module that enables companies to track their assets (machines, vehicles, computers) and manage maintenance requests for those assets. The module seamlessly connects **Equipment** (what is broken), **Teams** (who fix it), and **Requests** (the work to be done).

## ✨ Key Features

### 📦 Equipment Management
- **Central Asset Database**: Track all company assets with detailed information
- **Ownership Tracking**: Assign equipment to departments or employees
- **Location Management**: Know exactly where each asset is located
- **Warranty Tracking**: Monitor warranty status with automatic expiration detection
- **Smart Buttons**: Quick access to related maintenance requests

### 👥 Maintenance Teams
- **Specialized Teams**: Create teams for different specialties (Mechanics, Electricians, IT Support)
- **Team Members**: Assign technicians to teams
- **Team Dashboard**: Kanban view showing open requests and equipment count

### 🔧 Maintenance Requests
- **Request Types**:
  - 🔴 **Corrective**: Unplanned repairs for breakdowns
  - 🔵 **Preventive**: Planned maintenance and routine checkups
- **Auto-Fill Logic**: Automatically populate team and category when selecting equipment
- **Priority Levels**: Low, Normal, High, Urgent
- **Overdue Detection**: Visual indicators for overdue requests

## 🔄 Workflow

### Breakdown Flow (Corrective)
```
New Request → Select Equipment → Auto-fill Team → Assign Technician → In Progress → Record Hours → Repaired
```

### Routine Checkup Flow (Preventive)
```
Create Request → Set Type to Preventive → Schedule Date → Appears on Calendar → Complete Maintenance
```

## 📊 Views & Interface

### Kanban Board (Primary Workspace)
- Drag & drop cards between stages
- Visual indicators for technician avatar and overdue status
- Quick create functionality
- Grouped by: New | In Progress | Repaired | Scrap

### Calendar View
- See all scheduled maintenance at a glance
- Color-coded by team
- Click to create new requests

### Reports
- Pivot analysis by team and category
- Graph views for visual analysis

## 🤖 Smart Features

### Auto-Fill Logic
When selecting equipment:
- Equipment Category is automatically filled
- Maintenance Team is automatically assigned
- Default Technician can be pre-assigned

### Scrap Logic
- Moving a request to "Scrap" stage automatically:
  - Marks the equipment as scrapped
  - Records the scrap date
  - Logs the reason

### Smart Button
- Equipment form shows "Maintenance" button
- Displays count of open requests
- Opens filtered list of all requests for that equipment

## 📁 Module Structure

```
odoo-hackathon/
├── app.py                          # Flask application entry point
├── requirements.txt                # Python dependencies
├── comprehensive_backend_test.py   # Backend test suite
├── test_api_like_user.py          # API simulation tests
├── test_backend.sh                 # Quick test runner
├── BACKEND_TEST_REPORT.md         # Test results documentation
├── API_TEST_GUIDE.md              # API testing guide
├── backend/
│   ├── __init__.py
│   ├── config.py                   # Database configuration
│   ├── seed.py                     # Database seeder
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User authentication
│   │   ├── equipment_category.py  # Equipment categories
│   │   ├── equipment.py           # Equipment/assets
│   │   ├── maintenance_request.py # Maintenance requests
│   │   ├── maintenance_stage.py   # Request stages
│   │   └── maintenance_team.py    # Maintenance teams
│   └── routes/
│       ├── __init__.py
│       ├── auth.py                # Authentication routes
│       ├── api.py                 # REST API endpoints
│       └── views.py               # Web page routes
└── gearguard/                      # Odoo module
    ├── __init__.py
    ├── __manifest__.py
    ├── data/
    │   └── stage_data.xml         # Default stages
    ├── demo/
    │   └── demo_data.xml          # Demo data
    ├── models/
    │   ├── __init__.py
    │   ├── equipment_category.py  # Equipment categories
    │   ├── equipment.py           # Equipment/assets
    │   ├── maintenance_request.py # Maintenance requests
    │   ├── maintenance_stage.py   # Request stages
    │   └── maintenance_team.py    # Maintenance teams
    ├── security/
    │   ├── gearguard_security.xml # Security groups & rules
    │   └── ir.model.access.csv    # Access rights
    ├── static/
    │   ├── description/
    │   │   └── index.html
    │   └── src/css/
    │       └── gearguard.css      # Custom styles
    └── views/
        ├── equipment_category_views.xml
        ├── equipment_views.xml
        ├── maintenance_request_views.xml
        ├── maintenance_team_views.xml
        └── menu_views.xml
```

## 🔒 Security

### Backend Security
- **Password Hashing**: Werkzeug security for password storage
- **Session Management**: Flask-Session with server-side storage
- **CSRF Protection**: Built-in Flask security features
- **SQL Injection Prevention**: SQLAlchemy ORM parameterization

### User Roles & Permissions
| Role | Backend Access | Description |
|------|----------------|-------------|
| Admin | Full Access | Dashboard, reports, all CRUD operations |
| Manager | Equipment & Requests | Create/edit equipment and requests |
| User | Read Only | View equipment and requests only |

### Odoo Security Groups
| Group | Description |
|-------|-------------|
| User | View equipment, create requests |
| Technician | Manage assigned requests |
| Manager | Full access |

## 🚀 Installation & Setup

### Backend Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database**:
   - Update `backend/config.py` with your PostgreSQL credentials
   - Or set environment variables:
     ```bash
     export DB_NAME=your_database
     export DB_USER=your_user
     export DB_PASSWORD=your_password
     export DB_HOST=localhost
     export DB_PORT=5432
     ```

3. **Initialize Database**:
   ```bash
   python backend/seed.py
   ```

4. **Run Application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`

### Odoo Module Installation

1. Copy the `gearguard` folder to your Odoo addons directory
2. Update the apps list: `Settings > Apps > Update Apps List`
3. Search for "GearGuard" and click Install

## 📋 Dependencies

### Backend Dependencies
- `Flask==3.0.0` - Web framework
- `Flask-SQLAlchemy==3.1.1` - Database ORM
- `Flask-Login==0.6.3` - User authentication
- `Flask-Session==0.8.0` - Server-side session management
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `python-dotenv==1.0.0` - Environment variable management
- `requests==2.31.0` - HTTP library for API testing

### Odoo Module Dependencies
- `base` - Odoo base module
- `hr` - Human Resources (for department/employee assignment)
- `mail` - Discuss (for chatter and activity tracking)

## 🎨 Demo Data

The module includes demo data with:
- 3 Maintenance Teams (Mechanics, Electricians, IT Support)
- 5 Equipment Categories
- 7 Equipment items
- 6 Sample Maintenance Requests

## 🧪 Testing

### Backend Model Testing

Test all backend models, relationships, and data integrity:

```bash
python comprehensive_backend_test.py
```

**Test Coverage:**
- ✅ Database connectivity
- ✅ Model existence and structure
- ✅ Relationships and foreign keys
- ✅ Authentication system
- ✅ Model properties and methods
- ✅ Data integrity validation

**Results:** 11/11 tests passing (100%)

See [BACKEND_TEST_REPORT.md](BACKEND_TEST_REPORT.md) for detailed results.

### API Testing (User Simulation)

Test all API endpoints with realistic user workflows:

```bash
python test_api_like_user.py
```

**Test Scenarios:**
1. **Admin User Workflow** (11 tests)
   - Dashboard statistics
   - Equipment and team management
   - Calendar view
   - Report generation

2. **Manager Workflow** (10 tests)
   - CRUD operations on equipment
   - Create and manage maintenance requests
   - Kanban stage transitions
   - Advanced filtering

3. **Regular User Workflow** (3 tests)
   - Read-only access validation
   - Equipment browsing
   - Request viewing

**Results:** 24/24 tests passing (100%)

See [API_TEST_GUIDE.md](API_TEST_GUIDE.md) for detailed usage instructions.

### Quick Test Script

Run both backend and API tests:

```bash
./test_backend.sh
```

## 📝 License

This module is licensed under LGPL-3.

## 📚 Documentation

- [Backend Test Report](BACKEND_TEST_REPORT.md) - Comprehensive backend testing results and bug fixes
- [API Test Guide](API_TEST_GUIDE.md) - User simulation testing documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<div align="center">

**GearGuard** - Keep your assets running smoothly! 🛠️

Made with ❤️ by **Team QuantCoder** | GCET

*Odoo Hackathon 2025*

</div>
