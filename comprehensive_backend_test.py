#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comprehensive Backend Testing Script for GearGuard
Tests all models, routes, and business logic
"""
import sys
from datetime import datetime, timedelta
from app import create_app
from backend.models import (
    db, Equipment, EquipmentCategory,
    MaintenanceTeam, TeamMember,
    MaintenanceStage, MaintenanceRequest,
    User, Role, ActivityLog
)

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(msg, status='INFO'):
    """Print formatted test message"""
    if status == 'PASS':
        print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")
    elif status == 'FAIL':
        print(f"{Colors.RED}✗{Colors.RESET} {msg}")
    elif status == 'WARN':
        print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")
    else:
        print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")

def print_section(title):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def test_database_connection(app):
    """Test database connectivity"""
    print_section("DATABASE CONNECTION TEST")
    try:
        with app.app_context():
            db.session.execute(db.text('SELECT 1'))
            print_test("Database connection successful", "PASS")
            return True
    except Exception as e:
        print_test(f"Database connection failed: {e}", "FAIL")
        return False

def test_models_exist(app):
    """Test that all models can be imported and have tables"""
    print_section("MODELS EXISTENCE TEST")
    errors = []
    
    with app.app_context():
        models = [
            ('User', User),
            ('Role', Role),
            ('ActivityLog', ActivityLog),
            ('Equipment', Equipment),
            ('EquipmentCategory', EquipmentCategory),
            ('MaintenanceTeam', MaintenanceTeam),
            ('TeamMember', TeamMember),
            ('MaintenanceStage', MaintenanceStage),
            ('MaintenanceRequest', MaintenanceRequest),
        ]
        
        for name, model in models:
            try:
                count = model.query.count()
                print_test(f"{name} model exists ({count} records)", "PASS")
            except Exception as e:
                errors.append(f"{name}: {e}")
                print_test(f"{name} model failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_relationships(app):
    """Test model relationships"""
    print_section("MODEL RELATIONSHIPS TEST")
    errors = []
    
    with app.app_context():
        # Test Equipment relationships
        try:
            eq = Equipment.query.first()
            if eq:
                _ = eq.category
                print_test("Equipment -> Category relationship", "PASS")
                _ = eq.default_team
                print_test("Equipment -> Default Team relationship", "PASS")
                _ = eq.default_technician
                print_test("Equipment -> Default Technician relationship", "PASS")
                _ = eq.maintenance_requests
                print_test("Equipment -> Maintenance Requests relationship", "PASS")
            else:
                print_test("No equipment found for testing relationships", "WARN")
        except Exception as e:
            errors.append(f"Equipment relationships: {e}")
            print_test(f"Equipment relationships failed: {e}", "FAIL")
        
        # Test MaintenanceRequest relationships
        try:
            req = MaintenanceRequest.query.first()
            if req:
                _ = req.equipment
                print_test("MaintenanceRequest -> Equipment relationship", "PASS")
                _ = req.team
                print_test("MaintenanceRequest -> Team relationship", "PASS")
                _ = req.stage
                print_test("MaintenanceRequest -> Stage relationship", "PASS")
            else:
                print_test("No maintenance request found for testing relationships", "WARN")
        except Exception as e:
            errors.append(f"MaintenanceRequest relationships: {e}")
            print_test(f"MaintenanceRequest relationships failed: {e}", "FAIL")
        
        # Test Team relationships
        try:
            team = MaintenanceTeam.query.first()
            if team:
                _ = team.members
                print_test("MaintenanceTeam -> Members relationship", "PASS")
                _ = team.equipment
                print_test("MaintenanceTeam -> Equipment relationship", "PASS")
            else:
                print_test("No team found for testing relationships", "WARN")
        except Exception as e:
            errors.append(f"Team relationships: {e}")
            print_test(f"Team relationships failed: {e}", "FAIL")
        
        # Test User relationships
        try:
            user = User.query.first()
            if user:
                _ = user.role
                print_test("User -> Role relationship", "PASS")
                _ = user.team
                print_test("User -> Team relationship", "PASS")
            else:
                print_test("No user found for testing relationships", "WARN")
        except Exception as e:
            errors.append(f"User relationships: {e}")
            print_test(f"User relationships failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_user_authentication(app):
    """Test user authentication logic"""
    print_section("USER AUTHENTICATION TEST")
    errors = []
    
    with app.app_context():
        try:
            # Test password hashing
            user = User.query.filter_by(email='admin@gearguard.com').first()
            if user:
                # Test correct password
                if user.check_password('admin123'):
                    print_test("Password verification (correct password)", "PASS")
                else:
                    errors.append("Password verification failed for correct password")
                    print_test("Password verification (correct password)", "FAIL")
                
                # Test wrong password
                if not user.check_password('wrongpassword'):
                    print_test("Password verification (wrong password)", "PASS")
                else:
                    errors.append("Password verification failed for wrong password")
                    print_test("Password verification (wrong password)", "FAIL")
            else:
                errors.append("Admin user not found")
                print_test("Admin user not found", "FAIL")
        except Exception as e:
            errors.append(f"Authentication test: {e}")
            print_test(f"Authentication test failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_equipment_properties(app):
    """Test equipment model properties"""
    print_section("EQUIPMENT PROPERTIES TEST")
    errors = []
    
    with app.app_context():
        try:
            eq = Equipment.query.first()
            if eq:
                # Test warranty status
                try:
                    _ = eq.is_warranty_valid
                    print_test("Equipment.is_warranty_valid property", "PASS")
                except Exception as e:
                    errors.append(f"is_warranty_valid: {e}")
                    print_test(f"Equipment.is_warranty_valid failed: {e}", "FAIL")
                
                # Test status color
                try:
                    color = eq.status_color
                    if color in ['success', 'warning', 'danger', 'secondary']:
                        print_test("Equipment.status_color property", "PASS")
                    else:
                        errors.append(f"Invalid status_color: {color}")
                        print_test(f"Invalid status_color: {color}", "FAIL")
                except Exception as e:
                    errors.append(f"status_color: {e}")
                    print_test(f"Equipment.status_color failed: {e}", "FAIL")
                
                # Test open request count
                try:
                    count = eq.open_request_count
                    if isinstance(count, int) and count >= 0:
                        print_test(f"Equipment.open_request_count property ({count} requests)", "PASS")
                    else:
                        errors.append(f"Invalid open_request_count: {count}")
                        print_test(f"Invalid open_request_count: {count}", "FAIL")
                except Exception as e:
                    errors.append(f"open_request_count: {e}")
                    print_test(f"Equipment.open_request_count failed: {e}", "FAIL")
            else:
                print_test("No equipment found for testing properties", "WARN")
        except Exception as e:
            errors.append(f"Equipment properties: {e}")
            print_test(f"Equipment properties test failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_maintenance_request_properties(app):
    """Test maintenance request model properties"""
    print_section("MAINTENANCE REQUEST PROPERTIES TEST")
    errors = []
    
    with app.app_context():
        try:
            req = MaintenanceRequest.query.first()
            if req:
                # Test is_overdue
                try:
                    is_overdue = req.is_overdue
                    if isinstance(is_overdue, bool):
                        print_test(f"MaintenanceRequest.is_overdue property (overdue={is_overdue})", "PASS")
                    else:
                        errors.append(f"Invalid is_overdue type: {type(is_overdue)}")
                        print_test(f"Invalid is_overdue type: {type(is_overdue)}", "FAIL")
                except Exception as e:
                    errors.append(f"is_overdue: {e}")
                    print_test(f"MaintenanceRequest.is_overdue failed: {e}", "FAIL")
                
                # Test priority color
                try:
                    color = req.priority_color
                    if color in ['info', 'primary', 'warning', 'danger']:
                        print_test("MaintenanceRequest.priority_color property", "PASS")
                    else:
                        errors.append(f"Invalid priority_color: {color}")
                        print_test(f"Invalid priority_color: {color}", "FAIL")
                except Exception as e:
                    errors.append(f"priority_color: {e}")
                    print_test(f"MaintenanceRequest.priority_color failed: {e}", "FAIL")
                
                # Test priority icon
                try:
                    icon = req.priority_icon
                    if icon in ['arrow-down', 'minus', 'arrow-up', 'exclamation-triangle']:
                        print_test("MaintenanceRequest.priority_icon property", "PASS")
                    else:
                        errors.append(f"Invalid priority_icon: {icon}")
                        print_test(f"Invalid priority_icon: {icon}", "FAIL")
                except Exception as e:
                    errors.append(f"priority_icon: {e}")
                    print_test(f"MaintenanceRequest.priority_icon failed: {e}", "FAIL")
                
                # Test type icon
                try:
                    icon = req.type_icon
                    if icon in ['wrench', 'calendar-check']:
                        print_test("MaintenanceRequest.type_icon property", "PASS")
                    else:
                        errors.append(f"Invalid type_icon: {icon}")
                        print_test(f"Invalid type_icon: {icon}", "FAIL")
                except Exception as e:
                    errors.append(f"type_icon: {e}")
                    print_test(f"MaintenanceRequest.type_icon failed: {e}", "FAIL")
            else:
                print_test("No maintenance request found for testing properties", "WARN")
        except Exception as e:
            errors.append(f"MaintenanceRequest properties: {e}")
            print_test(f"MaintenanceRequest properties test failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_reference_generation(app):
    """Test automatic reference generation"""
    print_section("REFERENCE GENERATION TEST")
    errors = []
    
    with app.app_context():
        try:
            # Test Equipment code generation
            eq = Equipment.query.first()
            if eq and eq.code:
                if eq.code.startswith('EQ-'):
                    print_test(f"Equipment code generation: {eq.code}", "PASS")
                else:
                    errors.append(f"Invalid equipment code format: {eq.code}")
                    print_test(f"Invalid equipment code format: {eq.code}", "FAIL")
            else:
                print_test("No equipment with code found", "WARN")
            
            # Test MaintenanceRequest reference generation
            req = MaintenanceRequest.query.first()
            if req and req.reference:
                if req.reference.startswith('MR-'):
                    print_test(f"Maintenance request reference generation: {req.reference}", "PASS")
                else:
                    errors.append(f"Invalid request reference format: {req.reference}")
                    print_test(f"Invalid request reference format: {req.reference}", "FAIL")
            else:
                print_test("No maintenance request with reference found", "WARN")
        except Exception as e:
            errors.append(f"Reference generation: {e}")
            print_test(f"Reference generation test failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_role_permissions(app):
    """Test role permission system"""
    print_section("ROLE PERMISSIONS TEST")
    errors = []
    
    with app.app_context():
        try:
            roles = {
                'Admin': {
                    'can_manage_users': True,
                    'can_manage_teams': True,
                    'can_manage_equipment': True,
                    'can_manage_requests': True,
                    'can_manage_settings': True,
                    'can_view_reports': True,
                    'can_assign_requests': True,
                    'can_complete_requests': True,
                },
                'Manager': {
                    'can_manage_users': False,
                    'can_manage_teams': True,
                    'can_manage_equipment': True,
                    'can_manage_requests': True,
                    'can_manage_settings': False,
                    'can_view_reports': True,
                    'can_assign_requests': True,
                    'can_complete_requests': True,
                },
                'Technician': {
                    'can_manage_users': False,
                    'can_manage_teams': False,
                    'can_manage_equipment': False,
                    'can_manage_requests': False,
                    'can_manage_settings': False,
                    'can_view_reports': False,
                    'can_assign_requests': False,
                    'can_complete_requests': True,
                },
                'User': {
                    'can_manage_users': False,
                    'can_manage_teams': False,
                    'can_manage_equipment': False,
                    'can_manage_requests': False,
                    'can_manage_settings': False,
                    'can_view_reports': False,
                    'can_assign_requests': False,
                    'can_complete_requests': False,
                },
            }
            
            for role_name, expected_perms in roles.items():
                role = Role.query.filter_by(name=role_name).first()
                if role:
                    all_correct = True
                    for perm, expected in expected_perms.items():
                        actual = getattr(role, perm)
                        if actual != expected:
                            errors.append(f"{role_name}.{perm}: expected {expected}, got {actual}")
                            all_correct = False
                    
                    if all_correct:
                        print_test(f"Role '{role_name}' permissions correct", "PASS")
                    else:
                        print_test(f"Role '{role_name}' has incorrect permissions", "FAIL")
                else:
                    errors.append(f"Role '{role_name}' not found")
                    print_test(f"Role '{role_name}' not found", "FAIL")
        except Exception as e:
            errors.append(f"Role permissions: {e}")
            print_test(f"Role permissions test failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_data_integrity(app):
    """Test data integrity and constraints"""
    print_section("DATA INTEGRITY TEST")
    errors = []
    
    with app.app_context():
        try:
            # Test all equipment have categories
            eq_without_cat = Equipment.query.filter_by(category_id=None).count()
            if eq_without_cat == 0:
                print_test("All equipment have categories", "PASS")
            else:
                errors.append(f"{eq_without_cat} equipment without category")
                print_test(f"{eq_without_cat} equipment without category", "FAIL")
            
            # Test all maintenance requests have equipment
            req_without_eq = MaintenanceRequest.query.filter_by(equipment_id=None).count()
            if req_without_eq == 0:
                print_test("All maintenance requests have equipment", "PASS")
            else:
                errors.append(f"{req_without_eq} requests without equipment")
                print_test(f"{req_without_eq} requests without equipment", "FAIL")
            
            # Test all maintenance requests have teams
            req_without_team = MaintenanceRequest.query.filter_by(team_id=None).count()
            if req_without_team == 0:
                print_test("All maintenance requests have teams", "PASS")
            else:
                errors.append(f"{req_without_team} requests without team")
                print_test(f"{req_without_team} requests without team", "FAIL")
            
            # Test all maintenance requests have stages
            req_without_stage = MaintenanceRequest.query.filter_by(stage_id=None).count()
            if req_without_stage == 0:
                print_test("All maintenance requests have stages", "PASS")
            else:
                errors.append(f"{req_without_stage} requests without stage")
                print_test(f"{req_without_stage} requests without stage", "FAIL")
            
            # Test all users have roles
            users_without_role = User.query.filter_by(role_id=None).count()
            if users_without_role == 0:
                print_test("All users have roles", "PASS")
            else:
                errors.append(f"{users_without_role} users without role")
                print_test(f"{users_without_role} users without role", "FAIL")
        except Exception as e:
            errors.append(f"Data integrity: {e}")
            print_test(f"Data integrity test failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_stage_properties(app):
    """Test stage model properties"""
    print_section("STAGE PROPERTIES TEST")
    errors = []
    
    with app.app_context():
        try:
            # Test stage request count
            stage = MaintenanceStage.query.first()
            if stage:
                try:
                    count = stage.request_count
                    if isinstance(count, int) and count >= 0:
                        print_test(f"MaintenanceStage.request_count property ({count} requests)", "PASS")
                    else:
                        errors.append(f"Invalid request_count: {count}")
                        print_test(f"Invalid request_count: {count}", "FAIL")
                except Exception as e:
                    errors.append(f"request_count: {e}")
                    print_test(f"MaintenanceStage.request_count failed: {e}", "FAIL")
                
                # Test is_done and is_scrap flags
                completed_stage = MaintenanceStage.query.filter_by(is_done=True).first()
                if completed_stage:
                    print_test("Found 'completed' stage with is_done=True", "PASS")
                else:
                    print_test("No 'completed' stage found", "WARN")
                
                scrap_stage = MaintenanceStage.query.filter_by(is_scrap=True).first()
                if scrap_stage:
                    print_test("Found 'scrap' stage with is_scrap=True", "PASS")
                else:
                    print_test("No 'scrap' stage found", "WARN")
            else:
                print_test("No stage found for testing properties", "WARN")
        except Exception as e:
            errors.append(f"Stage properties: {e}")
            print_test(f"Stage properties test failed: {e}", "FAIL")
    
    return len(errors) == 0

def test_scrap_functionality(app):
    """Test equipment scrap functionality"""
    print_section("SCRAP FUNCTIONALITY TEST")
    errors = []
    
    with app.app_context():
        try:
            # Find a non-scrapped equipment
            eq = Equipment.query.filter_by(is_scrapped=False).first()
            if eq:
                # Test scrapping
                eq.is_scrapped = True
                eq.scrap_date = datetime.now()
                eq.scrap_reason = "Test scrap reason"
                db.session.commit()
                
                # Verify
                scrapped = Equipment.query.get(eq.id)
                if scrapped.is_scrapped and scrapped.scrap_date and scrapped.scrap_reason:
                    print_test("Equipment scrap functionality", "PASS")
                    
                    # Restore state
                    scrapped.is_scrapped = False
                    scrapped.scrap_date = None
                    scrapped.scrap_reason = None
                    db.session.commit()
                else:
                    errors.append("Scrap fields not set correctly")
                    print_test("Scrap fields not set correctly", "FAIL")
            else:
                print_test("No non-scrapped equipment found for testing", "WARN")
        except Exception as e:
            errors.append(f"Scrap functionality: {e}")
            print_test(f"Scrap functionality test failed: {e}", "FAIL")
            db.session.rollback()
    
    return len(errors) == 0

def run_all_tests():
    """Run all tests and return summary"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔═════════════════════════════════════════════════════════════╗")
    print("║                                                             ║")
    print("║     GEARGUARD COMPREHENSIVE BACKEND TEST SUITE              ║")
    print("║                                                             ║")
    print("╚═════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    app = create_app('development')
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Models Existence", test_models_exist),
        ("Model Relationships", test_relationships),
        ("User Authentication", test_user_authentication),
        ("Equipment Properties", test_equipment_properties),
        ("Maintenance Request Properties", test_maintenance_request_properties),
        ("Reference Generation", test_reference_generation),
        ("Role Permissions", test_role_permissions),
        ("Data Integrity", test_data_integrity),
        ("Stage Properties", test_stage_properties),
        ("Scrap Functionality", test_scrap_functionality),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func(app)
            results.append((name, passed))
        except Exception as e:
            print_test(f"Test '{name}' crashed: {e}", "FAIL")
            results.append((name, False))
    
    # Print summary
    print_section("TEST SUMMARY")
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print_test(f"{name}: {status}", status)
    
    print(f"\n{Colors.BOLD}")
    print(f"Total Tests: {total_count}")
    print(f"{Colors.GREEN}Passed: {passed_count}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {total_count - passed_count}{Colors.RESET}")
    
    if passed_count == total_count:
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}")
        print("ALL TESTS PASSED! ✓")
        print(f"{'='*60}{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}{'='*60}")
        print(f"SOME TESTS FAILED! {total_count - passed_count}/{total_count} failures")
        print(f"{'='*60}{Colors.RESET}\n")
        return 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
