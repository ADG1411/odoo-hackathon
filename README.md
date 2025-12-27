# GearGuard: The Ultimate Maintenance Tracker

![Odoo Version](https://img.shields.io/badge/Odoo-17.0-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green)

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
gearguard/
├── __init__.py
├── __manifest__.py
├── data/
│   └── stage_data.xml          # Default stages
├── demo/
│   └── demo_data.xml           # Demo data
├── models/
│   ├── __init__.py
│   ├── equipment_category.py   # Equipment categories
│   ├── equipment.py            # Equipment/assets
│   ├── maintenance_request.py  # Maintenance requests
│   ├── maintenance_stage.py    # Request stages
│   └── maintenance_team.py     # Maintenance teams
├── security/
│   ├── gearguard_security.xml  # Security groups & rules
│   └── ir.model.access.csv     # Access rights
├── static/
│   ├── description/
│   │   └── index.html
│   └── src/css/
│       └── gearguard.css       # Custom styles
└── views/
    ├── equipment_category_views.xml
    ├── equipment_views.xml
    ├── maintenance_request_views.xml
    ├── maintenance_team_views.xml
    └── menu_views.xml
```

## 🔒 Security

### Groups
| Group | Description |
|-------|-------------|
| User | View equipment, create requests |
| Technician | Manage assigned requests |
| Manager | Full access |

## 🚀 Installation

1. Copy the `gearguard` folder to your Odoo addons directory
2. Update the apps list: `Settings > Apps > Update Apps List`
3. Search for "GearGuard" and click Install

## 📋 Dependencies

- `base` - Odoo base module
- `hr` - Human Resources (for department/employee assignment)
- `mail` - Discuss (for chatter and activity tracking)

## 🎨 Demo Data

The module includes demo data with:
- 3 Maintenance Teams (Mechanics, Electricians, IT Support)
- 5 Equipment Categories
- 7 Equipment items
- 6 Sample Maintenance Requests

## 📝 License

This module is licensed under LGPL-3.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**GearGuard** - Keep your assets running smoothly! 🛠️