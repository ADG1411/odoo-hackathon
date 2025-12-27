#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GearGuard API User Simulation Script
Simulates real user interactions with the API
"""
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class GearGuardAPITester:
    def __init__(self, base_url: str = 'http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_user = None
        
    def print_step(self, step: str, emoji: str = "🔹"):
        print(f"\n{Colors.CYAN}{emoji} {step}{Colors.RESET}")
        
    def print_success(self, message: str):
        print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")
        
    def print_error(self, message: str):
        print(f"{Colors.RED}✗ {message}{Colors.RESET}")
        
    def print_data(self, label: str, data: dict):
        print(f"{Colors.YELLOW}{label}:{Colors.RESET}")
        print(json.dumps(data, indent=2, default=str))
        
    def print_header(self, title: str):
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.HEADER}{title:^60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*60}{Colors.RESET}\n")
        
    # ====================================================================================
    # AUTHENTICATION TESTS
    # ====================================================================================
    
    def test_login(self, email: str, password: str) -> bool:
        """Test user login"""
        self.print_step("Logging in as user", "🔐")
        
        try:
            response = self.session.post(
                f'{self.base_url}/auth/login',
                json={'email': email, 'password': password}
            )
            
            if response.status_code == 200:
                self.current_user = {'email': email}
                self.print_success(f"Login successful: {email}")
                return True
            else:
                self.print_error(f"Login failed: {response.status_code} - {response.text[:200]}")
                return False
        except Exception as e:
            self.print_error(f"Login error: {e}")
            return False
            
    def test_logout(self) -> bool:
        """Test user logout"""
        self.print_step("Logging out", "🚪")
        
        try:
            response = self.session.post(f'{self.base_url}/auth/logout')
            
            if response.status_code == 200:
                self.current_user = None
                self.print_success("Logout successful")
                return True
            else:
                self.print_error(f"Logout failed: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Logout error: {e}")
            return False
    
    # ====================================================================================
    # DASHBOARD TESTS
    # ====================================================================================
    
    def test_dashboard_stats(self) -> Optional[dict]:
        """Test dashboard statistics"""
        self.print_step("Fetching dashboard statistics", "📊")
        
        try:
            response = self.session.get(f'{self.base_url}/api/dashboard/stats')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Dashboard stats retrieved")
                self.print_data("Statistics", data)
                return data
            else:
                self.print_error(f"Failed to get stats: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Dashboard error: {e}")
            return None
            
    def test_requests_by_stage(self) -> Optional[dict]:
        """Test requests by stage chart data"""
        self.print_step("Fetching requests by stage", "📈")
        
        try:
            response = self.session.get(f'{self.base_url}/api/dashboard/requests-by-stage')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Requests by stage retrieved")
                self.print_data("Chart Data", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
    
    # ====================================================================================
    # EQUIPMENT TESTS
    # ====================================================================================
    
    def test_get_equipment_list(self) -> Optional[list]:
        """Test getting equipment list"""
        self.print_step("Fetching equipment list", "🔧")
        
        try:
            response = self.session.get(f'{self.base_url}/api/equipment')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Retrieved {len(data)} equipment items")
                if data:
                    self.print_data("Sample Equipment", data[0])
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
            
    def test_get_equipment_detail(self, equipment_id: int) -> Optional[dict]:
        """Test getting equipment detail"""
        self.print_step(f"Fetching equipment #{equipment_id} details", "🔍")
        
        try:
            response = self.session.get(f'{self.base_url}/api/equipment/{equipment_id}')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Equipment details: {data.get('name')}")
                self.print_data("Equipment Details", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
            
    def test_equipment_autofill(self, equipment_id: int) -> Optional[dict]:
        """Test equipment autofill for request creation"""
        self.print_step(f"Testing autofill for equipment #{equipment_id}", "✨")
        
        try:
            response = self.session.get(f'{self.base_url}/api/equipment/{equipment_id}/autofill')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Autofill data retrieved")
                self.print_data("Autofill Data", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
            
    def test_create_equipment(self, equipment_data: dict) -> Optional[dict]:
        """Test creating new equipment"""
        self.print_step("Creating new equipment", "➕")
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/equipment',
                json=equipment_data
            )
            
            if response.status_code == 201:
                data = response.json()
                self.print_success(f"Equipment created: {data.get('name')} ({data.get('code')})")
                self.print_data("New Equipment", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
    
    # ====================================================================================
    # MAINTENANCE REQUEST TESTS
    # ====================================================================================
    
    def test_get_requests(self, filters: Optional[dict] = None) -> Optional[list]:
        """Test getting maintenance requests with optional filters"""
        filter_str = f" with filters {filters}" if filters else ""
        self.print_step(f"Fetching maintenance requests{filter_str}", "📋")
        
        try:
            response = self.session.get(
                f'{self.base_url}/api/requests',
                params=filters or {}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Retrieved {len(data)} requests")
                if data:
                    self.print_data("Sample Request", data[0])
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
            
    def test_create_request(self, request_data: dict) -> Optional[dict]:
        """Test creating a new maintenance request"""
        self.print_step("Creating new maintenance request", "🆕")
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/requests',
                json=request_data
            )
            
            if response.status_code == 201:
                data = response.json()
                self.print_success(f"Request created: {data.get('reference')} - {data.get('name')}")
                self.print_data("New Request", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
            
    def test_update_request(self, request_id: int, update_data: dict) -> Optional[dict]:
        """Test updating a maintenance request"""
        self.print_step(f"Updating request #{request_id}", "✏️")
        
        try:
            response = self.session.put(
                f'{self.base_url}/api/requests/{request_id}',
                json=update_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Request updated: {data.get('reference')}")
                self.print_data("Updated Request", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
            
    def test_move_request_stage(self, request_id: int, new_stage_id: int) -> Optional[dict]:
        """Test moving request to different stage (Kanban drag & drop)"""
        self.print_step(f"Moving request #{request_id} to stage #{new_stage_id}", "🔄")
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/requests/{request_id}/move-stage',
                json={'stage_id': new_stage_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Request moved to: {data.get('stage_name')}")
                self.print_data("Updated Request", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
    
    # ====================================================================================
    # TEAM TESTS
    # ====================================================================================
    
    def test_get_teams(self) -> Optional[list]:
        """Test getting maintenance teams"""
        self.print_step("Fetching maintenance teams", "👥")
        
        try:
            response = self.session.get(f'{self.base_url}/api/teams')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Retrieved {len(data)} teams")
                if data:
                    self.print_data("Sample Team", data[0])
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
    
    # ====================================================================================
    # CALENDAR TESTS
    # ====================================================================================
    
    def test_calendar_events(self) -> Optional[list]:
        """Test getting calendar events"""
        self.print_step("Fetching calendar events", "📅")
        
        try:
            response = self.session.get(f'{self.base_url}/api/calendar/events')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Retrieved {len(data)} events")
                if data:
                    self.print_data("Sample Event", data[0])
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
    
    # ====================================================================================
    # REPORTS TESTS
    # ====================================================================================
    
    def test_reports_summary(self) -> Optional[dict]:
        """Test getting reports summary"""
        self.print_step("Fetching reports summary", "📄")
        
        try:
            response = self.session.get(f'{self.base_url}/api/reports/summary')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Reports summary retrieved")
                self.print_data("Summary", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None
            
    def test_equipment_breakdown(self) -> Optional[dict]:
        """Test equipment breakdown report"""
        self.print_step("Fetching equipment breakdown", "🔩")
        
        try:
            response = self.session.get(f'{self.base_url}/api/reports/equipment-breakdown')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success("Equipment breakdown retrieved")
                self.print_data("Breakdown", data)
                return data
            else:
                self.print_error(f"Failed: {response.status_code}")
                return None
        except Exception as e:
            self.print_error(f"Error: {e}")
            return None


def run_user_simulation():
    """Run complete user simulation"""
    tester = GearGuardAPITester()
    
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                                                               ║")
    print("║          GEARGUARD API USER SIMULATION TEST                   ║")
    print("║          Testing API Like a Real User                         ║")
    print("║                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    results = {
        'passed': 0,
        'failed': 0,
        'tests': []
    }
    
    def record_test(name: str, success: bool):
        results['tests'].append({'name': name, 'success': success})
        if success:
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # ====================================================================================
    # SCENARIO 1: ADMIN USER WORKFLOW
    # ====================================================================================
    
    tester.print_header("SCENARIO 1: Admin User Workflow")
    
    # Test 1: Login as admin
    success = tester.test_login('admin@gearguard.com', 'admin123')
    record_test('Admin Login', success)
    
    if success:
        # Test 2: View dashboard
        stats = tester.test_dashboard_stats()
        record_test('Dashboard Stats', stats is not None)
        
        # Test 3: View requests by stage
        chart_data = tester.test_requests_by_stage()
        record_test('Requests by Stage Chart', chart_data is not None)
        
        # Test 4: View equipment list
        equipment = tester.test_get_equipment_list()
        record_test('Equipment List', equipment is not None)
        
        # Test 5: View equipment detail
        if equipment:
            detail = tester.test_get_equipment_detail(equipment[0]['id'])
            record_test('Equipment Detail', detail is not None)
            
            # Test 6: Test autofill
            autofill = tester.test_equipment_autofill(equipment[0]['id'])
            record_test('Equipment Autofill', autofill is not None)
        
        # Test 7: View teams
        teams = tester.test_get_teams()
        record_test('Teams List', teams is not None)
        
        # Test 8: View calendar events
        events = tester.test_calendar_events()
        record_test('Calendar Events', events is not None)
        
        # Test 9: View reports
        summary = tester.test_reports_summary()
        record_test('Reports Summary', summary is not None)
        
        breakdown = tester.test_equipment_breakdown()
        record_test('Equipment Breakdown', breakdown is not None)
        
        # Test 10: Logout
        logout = tester.test_logout()
        record_test('Admin Logout', logout)
    
    # ====================================================================================
    # SCENARIO 2: MANAGER USER WORKFLOW
    # ====================================================================================
    
    tester.print_header("SCENARIO 2: Manager User Workflow")
    
    # Test 11: Login as manager
    success = tester.test_login('abhi.gabani@gearguard.com', 'password123')
    record_test('Manager Login', success)
    
    if success:
        # Test 12: Create new equipment
        new_equipment = {
            'name': 'Test Laptop for API',
            'category_id': 1,
            'serial_number': f'TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'model': 'API Test Model',
            'manufacturer': 'Test Corp',
            'location': 'Test Lab',
            'department': 'IT',
            'status': 'operational',
            'default_team_id': 1
        }
        created_eq = tester.test_create_equipment(new_equipment)
        record_test('Create Equipment', created_eq is not None)
        
        # Test 13: Create maintenance request
        if created_eq:
            new_request = {
                'name': 'Test Maintenance Request',
                'description': 'Created via API test simulation',
                'equipment_id': created_eq['id'],
                'team_id': 1,
                'stage_id': 1,
                'request_type': 'corrective',
                'priority': 'normal',
                'requester_name': 'API Tester',
                'requester_email': 'test@gearguard.com',
                'scheduled_date': (datetime.now() + timedelta(days=1)).isoformat()
            }
            created_req = tester.test_create_request(new_request)
            record_test('Create Request', created_req is not None)
            
            # Test 14: Update request
            if created_req:
                update_data = {
                    'priority': 'high',
                    'technician_notes': 'Updated via API test'
                }
                updated = tester.test_update_request(created_req['id'], update_data)
                record_test('Update Request', updated is not None)
                
                # Test 15: Move request to different stage (Kanban)
                moved = tester.test_move_request_stage(created_req['id'], 2)
                record_test('Move Request Stage', moved is not None)
        
        # Test 16: View all requests
        all_requests = tester.test_get_requests()
        record_test('View All Requests', all_requests is not None)
        
        # Test 17: Filter requests by priority
        high_priority = tester.test_get_requests({'priority': 'high'})
        record_test('Filter Requests by Priority', high_priority is not None)
        
        # Test 18: Filter requests by type
        corrective = tester.test_get_requests({'request_type': 'corrective'})
        record_test('Filter Requests by Type', corrective is not None)
        
        # Test 19: Logout
        logout = tester.test_logout()
        record_test('Manager Logout', logout)
    
    # ====================================================================================
    # SCENARIO 3: REGULAR USER WORKFLOW
    # ====================================================================================
    
    tester.print_header("SCENARIO 3: Regular User Workflow")
    
    # Test 20: Login as regular user
    success = tester.test_login('user@gearguard.com', 'user123')
    record_test('User Login', success)
    
    if success:
        # Test 21: View equipment (read-only)
        equipment = tester.test_get_equipment_list()
        record_test('User View Equipment', equipment is not None)
        
        # Test 22: View requests (read-only)
        requests = tester.test_get_requests()
        record_test('User View Requests', requests is not None)
        
        # Test 23: Logout
        logout = tester.test_logout()
        record_test('User Logout', logout)
    
    # ====================================================================================
    # FINAL SUMMARY
    # ====================================================================================
    
    tester.print_header("TEST SUMMARY")
    
    print(f"{Colors.BOLD}Total Tests: {results['passed'] + results['failed']}{Colors.RESET}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.RESET}")
    
    success_rate = (results['passed'] / (results['passed'] + results['failed']) * 100) if (results['passed'] + results['failed']) > 0 else 0
    print(f"{Colors.YELLOW}Success Rate: {success_rate:.1f}%{Colors.RESET}\n")
    
    print(f"{Colors.BOLD}Test Details:{Colors.RESET}")
    for test in results['tests']:
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if test['success'] else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"  {status} - {test['name']}")
    
    if results['failed'] == 0:
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}")
        print("ALL API TESTS PASSED! ✓")
        print(f"{'='*60}{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}{'='*60}")
        print(f"SOME TESTS FAILED! {results['failed']} failures")
        print(f"{'='*60}{Colors.RESET}\n")
        return 1


if __name__ == '__main__':
    import sys
    exit_code = run_user_simulation()
    sys.exit(exit_code)
