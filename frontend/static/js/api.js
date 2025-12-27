/**
 * GearGuard - API Integration Module
 * Connects Frontend with Backend API
 */

const API_BASE = '/api';

// ==================== API SERVICE ====================
const GearGuardAPI = {
  
  // ==================== DASHBOARD ====================
  dashboard: {
    async getStats() {
      try {
        const response = await fetch(`${API_BASE}/dashboard/stats`);
        if (!response.ok) throw new Error('Failed to fetch stats');
        return await response.json();
      } catch (error) {
        console.error('Dashboard stats error:', error);
        return null;
      }
    },
    
    async getRecentRequests() {
      try {
        const response = await fetch(`${API_BASE}/dashboard/recent-requests`);
        if (!response.ok) throw new Error('Failed to fetch recent requests');
        return await response.json();
      } catch (error) {
        console.error('Recent requests error:', error);
        return [];
      }
    },
    
    async getRequestsByStage() {
      try {
        const response = await fetch(`${API_BASE}/dashboard/requests-by-stage`);
        if (!response.ok) throw new Error('Failed to fetch requests by stage');
        return await response.json();
      } catch (error) {
        console.error('Requests by stage error:', error);
        return [];
      }
    },
    
    async getRequestsByPriority() {
      try {
        const response = await fetch(`${API_BASE}/dashboard/requests-by-priority`);
        if (!response.ok) throw new Error('Failed to fetch requests by priority');
        return await response.json();
      } catch (error) {
        console.error('Requests by priority error:', error);
        return [];
      }
    },
    
    async getEquipmentByStatus() {
      try {
        const response = await fetch(`${API_BASE}/dashboard/equipment-by-status`);
        if (!response.ok) throw new Error('Failed to fetch equipment by status');
        return await response.json();
      } catch (error) {
        console.error('Equipment by status error:', error);
        return [];
      }
    }
  },
  
  // ==================== EQUIPMENT ====================
  equipment: {
    async getAll(filters = {}) {
      try {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE}/equipment?${params}`);
        if (!response.ok) throw new Error('Failed to fetch equipment');
        return await response.json();
      } catch (error) {
        console.error('Equipment list error:', error);
        return [];
      }
    },
    
    async getById(id) {
      try {
        const response = await fetch(`${API_BASE}/equipment/${id}`);
        if (!response.ok) throw new Error('Failed to fetch equipment');
        return await response.json();
      } catch (error) {
        console.error('Equipment detail error:', error);
        return null;
      }
    },
    
    async create(data) {
      try {
        const response = await fetch(`${API_BASE}/equipment`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Failed to create equipment');
        }
        return await response.json();
      } catch (error) {
        console.error('Create equipment error:', error);
        throw error;
      }
    },
    
    async update(id, data) {
      try {
        const response = await fetch(`${API_BASE}/equipment/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Failed to update equipment');
        }
        return await response.json();
      } catch (error) {
        console.error('Update equipment error:', error);
        throw error;
      }
    },
    
    async delete(id) {
      try {
        const response = await fetch(`${API_BASE}/equipment/${id}`, {
          method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete equipment');
        return true;
      } catch (error) {
        console.error('Delete equipment error:', error);
        throw error;
      }
    },
    
    async getAutofill(id) {
      try {
        const response = await fetch(`${API_BASE}/equipment/${id}/autofill`);
        if (!response.ok) throw new Error('Failed to fetch autofill data');
        return await response.json();
      } catch (error) {
        console.error('Autofill error:', error);
        return null;
      }
    },
    
    async getRequests(id) {
      try {
        const response = await fetch(`${API_BASE}/equipment/${id}/requests`);
        if (!response.ok) throw new Error('Failed to fetch equipment requests');
        return await response.json();
      } catch (error) {
        console.error('Equipment requests error:', error);
        return null;
      }
    },
    
    async scrap(id, reason) {
      try {
        const response = await fetch(`${API_BASE}/equipment/${id}/scrap`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reason })
        });
        if (!response.ok) throw new Error('Failed to scrap equipment');
        return await response.json();
      } catch (error) {
        console.error('Scrap equipment error:', error);
        throw error;
      }
    },
    
    async getDepartments() {
      try {
        const response = await fetch(`${API_BASE}/equipment/departments`);
        if (!response.ok) throw new Error('Failed to fetch departments');
        return await response.json();
      } catch (error) {
        console.error('Departments error:', error);
        return [];
      }
    }
  },
  
  // ==================== CATEGORIES ====================
  categories: {
    async getAll() {
      try {
        const response = await fetch(`${API_BASE}/categories`);
        if (!response.ok) throw new Error('Failed to fetch categories');
        return await response.json();
      } catch (error) {
        console.error('Categories error:', error);
        return [];
      }
    },
    
    async create(data) {
      try {
        const response = await fetch(`${API_BASE}/categories`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to create category');
        return await response.json();
      } catch (error) {
        console.error('Create category error:', error);
        throw error;
      }
    },
    
    async update(id, data) {
      try {
        const response = await fetch(`${API_BASE}/categories/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to update category');
        return await response.json();
      } catch (error) {
        console.error('Update category error:', error);
        throw error;
      }
    },
    
    async delete(id) {
      try {
        const response = await fetch(`${API_BASE}/categories/${id}`, {
          method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete category');
        return true;
      } catch (error) {
        console.error('Delete category error:', error);
        throw error;
      }
    }
  },
  
  // ==================== TEAMS ====================
  teams: {
    async getAll() {
      try {
        const response = await fetch(`${API_BASE}/teams`);
        if (!response.ok) throw new Error('Failed to fetch teams');
        return await response.json();
      } catch (error) {
        console.error('Teams error:', error);
        return [];
      }
    },
    
    async getById(id) {
      try {
        const response = await fetch(`${API_BASE}/teams/${id}`);
        if (!response.ok) throw new Error('Failed to fetch team');
        return await response.json();
      } catch (error) {
        console.error('Team detail error:', error);
        return null;
      }
    },
    
    async create(data) {
      try {
        const response = await fetch(`${API_BASE}/teams`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to create team');
        return await response.json();
      } catch (error) {
        console.error('Create team error:', error);
        throw error;
      }
    },
    
    async update(id, data) {
      try {
        const response = await fetch(`${API_BASE}/teams/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to update team');
        return await response.json();
      } catch (error) {
        console.error('Update team error:', error);
        throw error;
      }
    },
    
    async delete(id) {
      try {
        const response = await fetch(`${API_BASE}/teams/${id}`, {
          method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete team');
        return true;
      } catch (error) {
        console.error('Delete team error:', error);
        throw error;
      }
    },
    
    async addMember(teamId, data) {
      try {
        const response = await fetch(`${API_BASE}/teams/${teamId}/members`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Failed to add member');
        return await response.json();
      } catch (error) {
        console.error('Add member error:', error);
        throw error;
      }
    },
    
    async removeMember(teamId, memberId) {
      try {
        const response = await fetch(`${API_BASE}/teams/${teamId}/members/${memberId}`, {
          method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to remove member');
        return true;
      } catch (error) {
        console.error('Remove member error:', error);
        throw error;
      }
    }
  },
  
  // ==================== STAGES ====================
  stages: {
    async getAll() {
      try {
        const response = await fetch(`${API_BASE}/stages`);
        if (!response.ok) throw new Error('Failed to fetch stages');
        return await response.json();
      } catch (error) {
        console.error('Stages error:', error);
        return [];
      }
    }
  },
  
  // ==================== MAINTENANCE REQUESTS ====================
  requests: {
    async getAll(filters = {}) {
      try {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE}/requests?${params}`);
        if (!response.ok) throw new Error('Failed to fetch requests');
        return await response.json();
      } catch (error) {
        console.error('Requests error:', error);
        return [];
      }
    },
    
    async getById(id) {
      try {
        const response = await fetch(`${API_BASE}/requests/${id}`);
        if (!response.ok) throw new Error('Failed to fetch request');
        return await response.json();
      } catch (error) {
        console.error('Request detail error:', error);
        return null;
      }
    },
    
    async create(data) {
      try {
        const response = await fetch(`${API_BASE}/requests`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Failed to create request');
        }
        return await response.json();
      } catch (error) {
        console.error('Create request error:', error);
        throw error;
      }
    },
    
    async update(id, data) {
      try {
        const response = await fetch(`${API_BASE}/requests/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Failed to update request');
        }
        return await response.json();
      } catch (error) {
        console.error('Update request error:', error);
        throw error;
      }
    },
    
    async delete(id) {
      try {
        const response = await fetch(`${API_BASE}/requests/${id}`, {
          method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete request');
        return true;
      } catch (error) {
        console.error('Delete request error:', error);
        throw error;
      }
    },
    
    async moveStage(id, stageId) {
      try {
        const response = await fetch(`${API_BASE}/requests/${id}/move-stage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ stage_id: stageId })
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Failed to move request');
        }
        return await response.json();
      } catch (error) {
        console.error('Move stage error:', error);
        throw error;
      }
    },
    
    async assign(id, teamId) {
      try {
        const response = await fetch(`${API_BASE}/requests/${id}/assign`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ team_id: teamId })
        });
        if (!response.ok) throw new Error('Failed to assign request');
        return await response.json();
      } catch (error) {
        console.error('Assign request error:', error);
        throw error;
      }
    }
  },
  
  // ==================== CALENDAR ====================
  calendar: {
    async getEvents(start, end) {
      try {
        const params = new URLSearchParams();
        if (start) params.append('start', start);
        if (end) params.append('end', end);
        const response = await fetch(`${API_BASE}/calendar/events?${params}`);
        if (!response.ok) throw new Error('Failed to fetch events');
        return await response.json();
      } catch (error) {
        console.error('Calendar events error:', error);
        return [];
      }
    }
  },
  
  // ==================== REPORTS ====================
  reports: {
    async getSummary() {
      try {
        const response = await fetch(`${API_BASE}/reports/summary`);
        if (!response.ok) throw new Error('Failed to fetch report summary');
        return await response.json();
      } catch (error) {
        console.error('Report summary error:', error);
        return null;
      }
    },
    
    async getEquipmentBreakdown() {
      try {
        const response = await fetch(`${API_BASE}/reports/equipment-breakdown`);
        if (!response.ok) throw new Error('Failed to fetch equipment breakdown');
        return await response.json();
      } catch (error) {
        console.error('Equipment breakdown error:', error);
        return null;
      }
    },
    
    async getMaintenanceTrends() {
      try {
        const response = await fetch(`${API_BASE}/reports/maintenance-trends`);
        if (!response.ok) throw new Error('Failed to fetch maintenance trends');
        return await response.json();
      } catch (error) {
        console.error('Maintenance trends error:', error);
        return [];
      }
    }
  },
  
  // ==================== AUTH ====================
  auth: {
    async login(email, password) {
      try {
        const response = await fetch('/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Login failed');
        }
        return await response.json();
      } catch (error) {
        console.error('Login error:', error);
        throw error;
      }
    },
    
    async logout() {
      try {
        const response = await fetch('/auth/logout', { method: 'POST' });
        if (!response.ok) throw new Error('Logout failed');
        return true;
      } catch (error) {
        console.error('Logout error:', error);
        throw error;
      }
    },
    
    async getCurrentUser() {
      try {
        const response = await fetch('/auth/me');
        if (!response.ok) return null;
        return await response.json();
      } catch (error) {
        console.error('Get user error:', error);
        return null;
      }
    },
    
    async signup(data) {
      try {
        const response = await fetch('/auth/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Signup failed');
        }
        return await response.json();
      } catch (error) {
        console.error('Signup error:', error);
        throw error;
      }
    }
  },
  
  // ==================== USERS ====================
  users: {
    async getTechnicians() {
      try {
        const response = await fetch(`${API_BASE}/users/technicians`);
        if (!response.ok) throw new Error('Failed to fetch technicians');
        return await response.json();
      } catch (error) {
        console.error('Technicians error:', error);
        return [];
      }
    },
    
    async getCurrentUser() {
      try {
        const response = await fetch('/auth/me');
        if (!response.ok) return null;
        return await response.json();
      } catch (error) {
        console.error('Get current user error:', error);
        return null;
      }
    },
    
    async updateProfile(data) {
      try {
        const response = await fetch(`${API_BASE}/users/profile`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Failed to update profile');
        }
        return await response.json();
      } catch (error) {
        console.error('Update profile error:', error);
        throw error;
      }
    },
    
    async changePassword(data) {
      try {
        const response = await fetch(`${API_BASE}/users/change-password`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Failed to change password');
        }
        return await response.json();
      } catch (error) {
        console.error('Change password error:', error);
        throw error;
      }
    }
  }
};

// Make API available globally
window.GearGuardAPI = GearGuardAPI;
