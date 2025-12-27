# API User Simulation Test Guide

## Overview
The `test_api_like_user.py` script simulates real user interactions with the GearGuard API, testing all major features through 3 different user roles.

## Quick Start

```bash
# 1. Start the Flask server
source venv/bin/activate
python app.py

# 2. In another terminal, run the API test
source venv/bin/activate
python test_api_like_user.py
```

## Test Scenarios

### Scenario 1: Admin User Workflow (11 tests)
Tests comprehensive admin access to all features:
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

**Test User:** `admin@gearguard.com` / `admin123`

### Scenario 2: Manager User Workflow (10 tests)
Tests manager capabilities for CRUD operations:
- ✅ Login as manager
- ✅ Create new equipment
- ✅ Create maintenance request
- ✅ Update request (change priority)
- ✅ Move request to different stage (Kanban)
- ✅ View all requests
- ✅ Filter requests by priority
- ✅ Filter requests by type
- ✅ Logout

**Test User:** `abhi.gabani@gearguard.com` / `password123`

### Scenario 3: Regular User Workflow (3 tests)
Tests read-only access for regular users:
- ✅ Login as user
- ✅ View equipment (read-only)
- ✅ View requests (read-only)
- ✅ Logout

**Test User:** `user@gearguard.com` / `user123`

## Test Coverage

### API Endpoints Tested
- **Authentication:** `/auth/login`, `/auth/logout`
- **Dashboard:** `/api/dashboard/stats`, `/api/dashboard/requests-by-stage`
- **Equipment:** `/api/equipment`, `/api/equipment/<id>`, `/api/equipment/<id>/autofill`
- **Requests:** `/api/requests`, `/api/requests/<id>/move-stage`
- **Teams:** `/api/teams`
- **Calendar:** `/api/calendar/events`
- **Reports:** `/api/reports/summary`, `/api/reports/equipment-breakdown`

### Features Tested
1. **User Authentication** - Login/logout with session management
2. **Dashboard Analytics** - Statistics and charts
3. **Equipment Management** - CRUD operations
4. **Request Management** - Create, update, filter
5. **Kanban Workflow** - Moving requests between stages
6. **Autofill Logic** - Pre-populate forms with equipment data
7. **Team Management** - View teams and members
8. **Calendar Integration** - Scheduled maintenance events
9. **Reports** - Summary and breakdown reports
10. **Role-Based Access** - Different permissions per role

## Output Example

```
╔═══════════════════════════════════════════════════════════════╗
║          GEARGUARD API USER SIMULATION TEST                   ║
║          Testing API Like a Real User                         ║
╚═══════════════════════════════════════════════════════════════╝

============================================================
              SCENARIO 1: Admin User Workflow               
============================================================

🔐 Logging in as user
✓ Login successful: admin@gearguard.com

📊 Fetching dashboard statistics
✓ Dashboard stats retrieved
Statistics:
{
  "equipment": {"total": 18, "operational": 14, ...},
  "requests": {"total": 14, "open": 11, ...}
}

... (continues with all tests)

============================================================
                        TEST SUMMARY                        
============================================================

Total Tests: 24
Passed: 24
Failed: 0
Success Rate: 100.0%

Test Details:
  ✓ PASS - Admin Login
  ✓ PASS - Dashboard Stats
  ... (all tests)

============================================================
ALL API TESTS PASSED! ✓
============================================================
```

## Customization

### Change Base URL
Edit the script to test against different servers:
```python
tester = GearGuardAPITester(base_url='http://your-server:5000')
```

### Add New Tests
Extend the `GearGuardAPITester` class with new test methods:
```python
def test_your_feature(self):
    """Test your new feature"""
    self.print_step("Testing feature", "🔍")
    response = self.session.get(f'{self.base_url}/api/your-endpoint')
    # ... assertions
```

### Modify Test Data
Update the test data in `run_user_simulation()`:
```python
new_equipment = {
    'name': 'Your Equipment Name',
    'category_id': 1,
    # ... other fields
}
```

## Requirements

- Python 3.8+
- Flask server running on localhost:5000
- Required packages: `requests`, `json`, `datetime`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Troubleshooting

### Server Not Running
```
Error: Connection refused
```
**Solution:** Start the Flask server first with `python app.py`

### Authentication Failed
```
✗ Login failed: 401
```
**Solution:** Verify credentials match seeded users in database

### API Changes
If endpoints change, update the test methods in `test_api_like_user.py`

## Integration with CI/CD

Add to your GitHub Actions workflow:
```yaml
- name: Run API Tests
  run: |
    python app.py &
    sleep 5
    python test_api_like_user.py
```

## Next Steps

1. Add more test scenarios for edge cases
2. Implement assertion checks for response data
3. Add performance timing for each API call
4. Export test results to JSON/XML format
5. Integrate with testing frameworks (pytest, unittest)
