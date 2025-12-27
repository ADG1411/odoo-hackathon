/**
 * GearGuard - Main Application JavaScript
 * Modern Industrial SaaS UI Interactions
 */

// ==================== LOGOUT HANDLER ====================
async function handleLogout(event) {
  if (event) {
    event.preventDefault();
  }
  try {
    await GearGuardAPI.auth.logout();
    window.location.href = '/login';
  } catch (error) {
    console.error('Logout failed:', error);
    // Even if logout fails, redirect to login
    window.location.href = '/login';
  }
}

// ==================== SIDEBAR USER INFO ====================
async function loadSidebarUserInfo() {
  try {
    const data = await GearGuardAPI.users.getCurrentUser();
    const user = data?.user || data;
    
    if (user) {
      // Get proper name
      const userName = user.full_name || 
        (user.first_name && user.last_name ? 
          `${user.first_name} ${user.last_name}` : 
          user.email?.split('@')[0] || 'User');
      
      // Get role name (handle role as object or string)
      let roleName = 'User';
      if (user.role) {
        roleName = typeof user.role === 'object' ? user.role.name : user.role;
      }
      
      // Get initials
      const initials = userName.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'U';
      
      // Update sidebar elements
      const displayName = document.getElementById('user-display-name');
      const displayRole = document.getElementById('user-display-role');
      const userInitials = document.getElementById('user-initials');
      
      if (displayName) displayName.textContent = userName;
      if (displayRole) displayRole.textContent = roleName;
      if (userInitials) userInitials.textContent = initials;
    }
  } catch (error) {
    console.error('Failed to load sidebar user info:', error);
  }
}

// Load sidebar user info when DOM is ready
document.addEventListener('DOMContentLoaded', loadSidebarUserInfo);

// ==================== TOAST NOTIFICATIONS ====================
function showToast(title, message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  
  const icons = {
    success: 'check-circle',
    error: 'x-circle',
    warning: 'alert-triangle',
    info: 'info'
  };
  
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <i data-lucide="${icons[type]}" class="toast-icon"></i>
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove()">
      <i data-lucide="x" style="width: 16px; height: 16px;"></i>
    </button>
  `;
  
  container.appendChild(toast);
  
  // Initialize icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
  
  // Trigger animation
  requestAnimationFrame(() => {
    toast.classList.add('show');
  });
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 5000);
}

// ==================== LOADING STATES ====================
function showLoading(element) {
  if (!element) return;
  element.dataset.originalContent = element.innerHTML;
  element.classList.add('btn-loading');
  element.disabled = true;
}

function hideLoading(element) {
  if (!element) return;
  element.classList.remove('btn-loading');
  element.disabled = false;
  if (element.dataset.originalContent) {
    element.innerHTML = element.dataset.originalContent;
  }
}

// ==================== SKELETON LOADERS ====================
function showSkeleton(container, count = 3, type = 'card') {
  if (!container) return;
  
  let html = '';
  for (let i = 0; i < count; i++) {
    if (type === 'card') {
      html += `
        <div class="card" style="padding: var(--space-lg);">
          <div class="skeleton skeleton-title"></div>
          <div class="skeleton skeleton-text"></div>
          <div class="skeleton skeleton-text"></div>
          <div class="skeleton skeleton-text"></div>
        </div>
      `;
    } else if (type === 'list') {
      html += `
        <div class="flex items-center gap-md" style="padding: var(--space-md) 0;">
          <div class="skeleton skeleton-avatar"></div>
          <div style="flex: 1;">
            <div class="skeleton skeleton-text" style="width: 60%;"></div>
            <div class="skeleton skeleton-text" style="width: 40%;"></div>
          </div>
        </div>
      `;
    }
  }
  
  container.innerHTML = html;
}

function hideSkeleton(container, content) {
  if (!container) return;
  container.innerHTML = content;
}

// ==================== FORM VALIDATION ====================
function validateField(input) {
  const value = input.value.trim();
  const type = input.type;
  const required = input.required;
  
  // Clear previous errors
  input.classList.remove('error');
  const errorEl = input.parentElement.querySelector('.form-error');
  if (errorEl) errorEl.textContent = '';
  
  // Required check
  if (required && !value) {
    showFieldError(input, 'This field is required');
    return false;
  }
  
  // Email validation
  if (type === 'email' && value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      showFieldError(input, 'Please enter a valid email address');
      return false;
    }
  }
  
  // Password validation
  if (type === 'password' && value && input.minLength) {
    if (value.length < input.minLength) {
      showFieldError(input, `Password must be at least ${input.minLength} characters`);
      return false;
    }
  }
  
  return true;
}

function showFieldError(input, message) {
  input.classList.add('error');
  const errorEl = input.parentElement.querySelector('.form-error');
  if (errorEl) {
    errorEl.textContent = message;
  }
}

function clearFormErrors(form) {
  if (!form) return;
  
  form.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(input => {
    input.classList.remove('error');
  });
  
  form.querySelectorAll('.form-error').forEach(error => {
    error.textContent = '';
  });
}

// ==================== DATE FORMATTING ====================
function formatDate(date, format = 'short') {
  const d = new Date(date);
  
  if (format === 'short') {
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }
  
  if (format === 'long') {
    return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
  }
  
  if (format === 'time') {
    return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  }
  
  if (format === 'relative') {
    const now = new Date();
    const diff = now - d;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (seconds < 60) return 'Just now';
    if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (days < 7) return `${days} day${days > 1 ? 's' : ''} ago`;
    
    return formatDate(date, 'short');
  }
  
  return d.toLocaleDateString();
}

// ==================== API HELPERS ====================
async function apiRequest(url, options = {}) {
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  const config = { ...defaultOptions, ...options };
  
  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || data.message || 'Request failed');
    }
    
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// ==================== MODAL HELPERS ====================
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// ==================== DEBOUNCE & THROTTLE ====================
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function throttle(func, limit) {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// ==================== LOCAL STORAGE HELPERS ====================
function saveToStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    console.error('Failed to save to localStorage:', e);
  }
}

function loadFromStorage(key, defaultValue = null) {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (e) {
    console.error('Failed to load from localStorage:', e);
    return defaultValue;
  }
}

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', function() {
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
  
  // Add focus states to inputs
  document.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });
    
    input.addEventListener('blur', function() {
      this.parentElement.classList.remove('focused');
      validateField(this);
    });
  });
  
  // Add card hover effects
  document.querySelectorAll('.card:not(.card-static)').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-4px)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = '';
    });
  });
  
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
  
  // Auto-dismiss alerts
  document.querySelectorAll('.alert[data-dismiss]').forEach(alert => {
    const timeout = parseInt(alert.dataset.dismiss) || 5000;
    setTimeout(() => {
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    }, timeout);
  });
});

// ==================== KEYBOARD SHORTCUTS ====================
document.addEventListener('keydown', function(e) {
  // Escape to close modals
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(modal => {
      modal.classList.remove('active');
    });
    document.querySelectorAll('.side-panel.active').forEach(panel => {
      panel.classList.remove('active');
    });
    document.querySelectorAll('.side-panel-overlay.active').forEach(overlay => {
      overlay.classList.remove('active');
    });
    document.body.style.overflow = '';
  }
  
  // Ctrl/Cmd + K for search
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.focus();
    }
  }
});

// ==================== RESPONSIVE HELPERS ====================
function isMobile() {
  return window.innerWidth < 768;
}

function isTablet() {
  return window.innerWidth >= 768 && window.innerWidth < 1024;
}

function isDesktop() {
  return window.innerWidth >= 1024;
}

// ==================== EXPORT FOR MODULE USE ====================
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    showToast,
    showLoading,
    hideLoading,
    validateField,
    formatDate,
    apiRequest,
    debounce,
    throttle,
    saveToStorage,
    loadFromStorage
  };
}
