/**
 * GearGuard - Requests Page JavaScript
 * Handles request listing, filtering, and CRUD operations
 */

// Page state
let requestsState = {
  requests: [],
  stages: [],
  teams: [],
  equipment: [],
  categories: [],
  filters: {
    search: '',
    priority: '',
    stage_id: '',
    team_id: '',
    request_type: ''
  },
  currentRequest: null
};

// Initialize the page
async function initRequestsPage() {
  showLoading();
  
  try {
    // Load all required data in parallel
    const [requests, stages, teams, equipment, categories] = await Promise.all([
      GearGuardAPI.requests.getAll(),
      GearGuardAPI.stages.getAll(),
      GearGuardAPI.teams.getAll(),
      GearGuardAPI.equipment.getAll(),
      GearGuardAPI.categories.getAll()
    ]);
    
    requestsState.requests = requests || [];
    requestsState.stages = stages || [];
    requestsState.teams = teams || [];
    requestsState.equipment = equipment || [];
    requestsState.categories = categories || [];
    
    // Populate filter dropdowns
    populateFilterDropdowns();
    
    // Populate form dropdowns
    populateFormDropdowns();
    
    // Render requests
    renderRequests();
    
    // Update stats bar
    updateStatsBar();
    
  } catch (error) {
    console.error('Failed to initialize requests page:', error);
    showToast('Error', 'Failed to load requests data', 'error');
  }
  
  hideLoading();
}

// Populate filter dropdowns
function populateFilterDropdowns() {
  // Status/Stage filter
  const statusFilter = document.getElementById('filter-status');
  if (statusFilter) {
    statusFilter.innerHTML = '<option value="">All Status</option>';
    requestsState.stages.forEach(stage => {
      statusFilter.innerHTML += `<option value="${stage.id}">${stage.name}</option>`;
    });
  }
  
  // Team filter (if exists)
  const teamFilter = document.getElementById('filter-team');
  if (teamFilter) {
    teamFilter.innerHTML = '<option value="">All Teams</option>';
    requestsState.teams.forEach(team => {
      teamFilter.innerHTML += `<option value="${team.id}">${team.name}</option>`;
    });
  }
}

// Populate form dropdowns
function populateFormDropdowns() {
  // Equipment dropdown
  const equipmentSelect = document.getElementById('equipment-select');
  if (equipmentSelect) {
    equipmentSelect.innerHTML = '<option value="">Select Equipment</option>';
    requestsState.equipment.forEach(eq => {
      equipmentSelect.innerHTML += `<option value="${eq.id}">${eq.code} - ${eq.name}</option>`;
    });
  }
  
  // Team dropdown
  const teamSelect = document.getElementById('team-select');
  if (teamSelect) {
    teamSelect.innerHTML = '<option value="">Select Team</option>';
    requestsState.teams.forEach(team => {
      teamSelect.innerHTML += `<option value="${team.id}">${team.name}</option>`;
    });
  }
  
  // Stage dropdown
  const stageSelect = document.getElementById('stage-select');
  if (stageSelect) {
    stageSelect.innerHTML = '';
    requestsState.stages.forEach(stage => {
      stageSelect.innerHTML += `<option value="${stage.id}">${stage.name}</option>`;
    });
  }
}

// Render requests list
function renderRequests() {
  const container = document.getElementById('request-grid');
  if (!container) return;
  
  // Apply filters
  let filtered = requestsState.requests.filter(req => {
    const matchesSearch = !requestsState.filters.search || 
      req.name.toLowerCase().includes(requestsState.filters.search.toLowerCase()) ||
      req.reference.toLowerCase().includes(requestsState.filters.search.toLowerCase()) ||
      (req.equipment_name && req.equipment_name.toLowerCase().includes(requestsState.filters.search.toLowerCase()));
    
    const matchesPriority = !requestsState.filters.priority || 
      req.priority === requestsState.filters.priority;
    
    const matchesStage = !requestsState.filters.stage_id || 
      req.stage_id == requestsState.filters.stage_id;
    
    const matchesTeam = !requestsState.filters.team_id || 
      req.team_id == requestsState.filters.team_id;
    
    const matchesType = !requestsState.filters.request_type || 
      req.request_type === requestsState.filters.request_type;
    
    return matchesSearch && matchesPriority && matchesStage && matchesTeam && matchesType;
  });
  
  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 60px 20px;">
        <i data-lucide="clipboard-list" style="width: 48px; height: 48px; color: var(--text-muted); margin-bottom: 16px;"></i>
        <h3 style="color: var(--text-primary); margin-bottom: 8px;">No Requests Found</h3>
        <p style="color: var(--text-muted);">Try adjusting your filters or create a new request.</p>
        <button class="btn btn-primary" style="margin-top: 16px;" onclick="openCreateModal()">
          <i data-lucide="plus" style="width: 18px; height: 18px;"></i>
          Create Request
        </button>
      </div>
    `;
    lucide.createIcons();
    return;
  }
  
  container.innerHTML = filtered.map(req => createRequestCard(req)).join('');
  lucide.createIcons();
}

// Create request card HTML
function createRequestCard(req) {
  const priorityClass = getPriorityClass(req.priority);
  const priorityIcon = getPriorityIcon(req.priority);
  const typeIcon = req.request_type === 'corrective' ? 'wrench' : 'calendar-check';
  const stageName = req.stage_name || 'New';
  const stageColor = req.stage_color || '#6c757d';
  const scheduleDate = req.scheduled_date ? formatDate(req.scheduled_date, 'short') : 'Not scheduled';
  const duration = req.duration_hours ? `${req.duration_hours} hours` : 'TBD';
  const equipmentName = req.equipment_name || 'Unknown Equipment';
  const teamName = req.team_name || 'Unassigned';
  const requesterName = req.requester_name || 'Unknown';
  const initials = getInitials(requesterName);
  const overdueClass = req.is_overdue ? 'overdue' : '';
  
  return `
    <div class="request-card ${overdueClass}" data-id="${req.id}" data-priority="${req.priority}" data-status="${req.stage_id}">
      <div class="request-card-header">
        <div class="request-equipment">
          <div class="request-equipment-icon" style="background: ${getLightColor(stageColor)}; color: ${stageColor};">
            <i data-lucide="${typeIcon}" style="width: 24px; height: 24px;"></i>
          </div>
          <div class="request-equipment-info">
            <h4>${equipmentName}</h4>
            <span class="request-reference">${req.reference}</span>
          </div>
        </div>
        <span class="badge ${priorityClass}">
          <i data-lucide="${priorityIcon}" style="width: 12px; height: 12px;"></i>
          ${capitalizeFirst(req.priority)}
        </span>
      </div>
      <div class="request-card-body">
        <div class="request-meta">
          <div class="request-meta-item">
            <span class="request-meta-label">Type</span>
            <span class="request-meta-value">
              <i data-lucide="${typeIcon}" style="width: 14px; height: 14px;"></i>
              ${capitalizeFirst(req.request_type)}
            </span>
          </div>
          <div class="request-meta-item">
            <span class="request-meta-label">Status</span>
            <span class="request-meta-value">
              <span class="status-dot" style="background: ${stageColor};"></span>
              ${stageName}
            </span>
          </div>
          <div class="request-meta-item">
            <span class="request-meta-label">Scheduled</span>
            <span class="request-meta-value">${scheduleDate}</span>
          </div>
          <div class="request-meta-item">
            <span class="request-meta-label">Team</span>
            <span class="request-meta-value">${teamName}</span>
          </div>
        </div>
        <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5; margin-top: 12px;">
          ${req.name}${req.description ? ': ' + truncate(req.description, 100) : ''}
        </p>
        ${req.is_overdue ? '<div class="overdue-badge"><i data-lucide="alert-circle"></i> Overdue</div>' : ''}
      </div>
      <div class="request-card-footer">
        <div class="request-assignee">
          <div class="avatar avatar-sm">${initials}</div>
          <span>${requesterName}</span>
        </div>
        <div class="request-actions">
          <button class="btn btn-ghost btn-icon-sm" title="View" onclick="viewRequest(${req.id})">
            <i data-lucide="eye" style="width: 16px; height: 16px;"></i>
          </button>
          <button class="btn btn-ghost btn-icon-sm" title="Edit" onclick="editRequest(${req.id})">
            <i data-lucide="pencil" style="width: 16px; height: 16px;"></i>
          </button>
          <button class="btn btn-ghost btn-icon-sm" title="Move Stage" onclick="showMoveStageMenu(${req.id}, event)">
            <i data-lucide="git-branch" style="width: 16px; height: 16px;"></i>
          </button>
        </div>
      </div>
    </div>
  `;
}

// Update stats bar
function updateStatsBar() {
  const requests = requestsState.requests;
  const stages = requestsState.stages;
  
  // Count by stage
  const stageCounts = {};
  stages.forEach(s => stageCounts[s.id] = 0);
  requests.forEach(r => {
    if (r.stage_id && stageCounts[r.stage_id] !== undefined) {
      stageCounts[r.stage_id]++;
    }
  });
  
  // Update UI elements if they exist
  const newStage = stages.find(s => s.name.toLowerCase() === 'new');
  const progressStage = stages.find(s => s.name.toLowerCase().includes('progress'));
  const doneStage = stages.find(s => s.is_done);
  
  // Update counts in info bar
  const elements = document.querySelectorAll('.info-bar-item .info-bar-value');
  if (elements.length >= 4) {
    elements[0].textContent = newStage ? stageCounts[newStage.id] || 0 : 0;
    elements[1].textContent = progressStage ? stageCounts[progressStage.id] || 0 : 0;
    // Scheduled = preventive type
    elements[2].textContent = requests.filter(r => r.request_type === 'preventive').length;
    elements[3].textContent = doneStage ? stageCounts[doneStage.id] || 0 : 0;
  }
}

// Filter requests
function filterRequests() {
  requestsState.filters.search = document.getElementById('search-input')?.value || '';
  requestsState.filters.priority = document.getElementById('filter-priority')?.value || '';
  requestsState.filters.stage_id = document.getElementById('filter-status')?.value || '';
  requestsState.filters.team_id = document.getElementById('filter-team')?.value || '';
  
  renderRequests();
}

// Open create modal
async function openCreateModal() {
  requestsState.currentRequest = null;
  
  const modal = document.getElementById('request-modal');
  const modalTitle = document.getElementById('modal-title');
  const form = document.getElementById('request-form');
  
  if (modalTitle) modalTitle.textContent = 'Create New Request';
  if (form) form.reset();
  
  // Populate dropdowns if not already done
  populateFormDropdowns();
  
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

// Edit request
async function editRequest(id) {
  const request = requestsState.requests.find(r => r.id === id);
  if (!request) {
    // Fetch from API
    const req = await GearGuardAPI.requests.getById(id);
    if (!req) {
      showToast('Error', 'Request not found', 'error');
      return;
    }
    requestsState.currentRequest = req;
  } else {
    requestsState.currentRequest = request;
  }
  
  const modal = document.getElementById('request-modal');
  const modalTitle = document.getElementById('modal-title');
  
  if (modalTitle) modalTitle.textContent = `Edit Request ${requestsState.currentRequest.reference}`;
  
  // Populate form with current data
  populateEditForm(requestsState.currentRequest);
  
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

// Populate edit form
function populateEditForm(req) {
  const form = document.getElementById('request-form');
  if (!form) return;
  
  // Set form values
  setFormValue('request-name', req.name);
  setFormValue('request-description', req.description);
  setFormValue('equipment-select', req.equipment_id);
  setFormValue('team-select', req.team_id);
  setFormValue('stage-select', req.stage_id);
  setFormValue('priority-select', req.priority);
  setFormValue('type-select', req.request_type);
  setFormValue('scheduled-date', req.scheduled_date ? req.scheduled_date.split('T')[0] : '');
  setFormValue('deadline', req.deadline ? req.deadline.split('T')[0] : '');
  setFormValue('duration-hours', req.duration_hours);
  setFormValue('requester-name', req.requester_name);
  setFormValue('requester-email', req.requester_email);
  setFormValue('technician-notes', req.technician_notes);
  setFormValue('resolution', req.resolution);
}

// Helper to set form values
function setFormValue(id, value) {
  const el = document.getElementById(id);
  if (el && value !== undefined && value !== null) {
    el.value = value;
  }
}

// View request details
async function viewRequest(id) {
  const request = requestsState.requests.find(r => r.id === id) || 
                  await GearGuardAPI.requests.getById(id);
  
  if (!request) {
    showToast('Error', 'Request not found', 'error');
    return;
  }
  
  // Open detail panel
  const panel = document.getElementById('detail-panel');
  if (panel) {
    populateDetailPanel(request);
    panel.classList.add('active');
  }
}

// Populate detail panel
function populateDetailPanel(req) {
  const panel = document.getElementById('detail-panel');
  if (!panel) return;
  
  // Update panel content with request details
  const content = panel.querySelector('.panel-content');
  if (content) {
    content.innerHTML = `
      <div class="detail-section">
        <h4>${req.reference}</h4>
        <h2>${req.name}</h2>
        <p class="text-muted">${req.description || 'No description'}</p>
      </div>
      
      <div class="detail-section">
        <div class="detail-row">
          <span class="detail-label">Equipment</span>
          <span class="detail-value">${req.equipment_name || 'N/A'}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Team</span>
          <span class="detail-value">${req.team_name || 'Unassigned'}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Status</span>
          <span class="badge" style="background: ${req.stage_color}">${req.stage_name}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Priority</span>
          <span class="badge ${getPriorityClass(req.priority)}">${capitalizeFirst(req.priority)}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Type</span>
          <span class="detail-value">${capitalizeFirst(req.request_type)}</span>
        </div>
      </div>
      
      <div class="detail-section">
        <div class="detail-row">
          <span class="detail-label">Scheduled</span>
          <span class="detail-value">${req.scheduled_date ? formatDate(req.scheduled_date, 'long') : 'Not scheduled'}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Deadline</span>
          <span class="detail-value ${req.is_overdue ? 'text-danger' : ''}">${req.deadline ? formatDate(req.deadline, 'long') : 'No deadline'}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Duration</span>
          <span class="detail-value">${req.duration_hours ? req.duration_hours + ' hours' : 'TBD'}</span>
        </div>
      </div>
      
      <div class="detail-actions">
        <button class="btn btn-primary" onclick="editRequest(${req.id}); closePanel();">
          <i data-lucide="pencil"></i> Edit
        </button>
        <button class="btn btn-secondary" onclick="showMoveStageMenu(${req.id}, event)">
          <i data-lucide="git-branch"></i> Move Stage
        </button>
      </div>
    `;
    lucide.createIcons();
  }
}

// Submit request form
async function submitRequest() {
  const form = document.getElementById('request-form');
  if (!form) return;
  
  // Gather form data
  const data = {
    name: document.getElementById('request-name')?.value,
    description: document.getElementById('request-description')?.value,
    equipment_id: document.getElementById('equipment-select')?.value || null,
    team_id: document.getElementById('team-select')?.value || null,
    stage_id: document.getElementById('stage-select')?.value || null,
    priority: document.getElementById('priority-select')?.value || 'normal',
    request_type: document.getElementById('type-select')?.value || 'corrective',
    scheduled_date: document.getElementById('scheduled-date')?.value || null,
    deadline: document.getElementById('deadline')?.value || null,
    duration_hours: document.getElementById('duration-hours')?.value || null,
    requester_name: document.getElementById('requester-name')?.value,
    requester_email: document.getElementById('requester-email')?.value,
    technician_notes: document.getElementById('technician-notes')?.value,
    resolution: document.getElementById('resolution')?.value
  };
  
  // Validate required fields
  if (!data.name) {
    showToast('Error', 'Please enter a request name', 'error');
    return;
  }
  
  try {
    let result;
    if (requestsState.currentRequest) {
      // Update existing
      result = await GearGuardAPI.requests.update(requestsState.currentRequest.id, data);
      showToast('Success', 'Request updated successfully', 'success');
    } else {
      // Create new
      result = await GearGuardAPI.requests.create(data);
      showToast('Success', 'Request created successfully', 'success');
    }
    
    closeModal();
    
    // Refresh data
    await initRequestsPage();
    
  } catch (error) {
    showToast('Error', error.message || 'Failed to save request', 'error');
  }
}

// Move request to different stage
async function moveToStage(requestId, stageId) {
  try {
    await GearGuardAPI.requests.moveStage(requestId, stageId);
    
    const stageName = requestsState.stages.find(s => s.id == stageId)?.name || 'new stage';
    showToast('Success', `Request moved to ${stageName}`, 'success');
    
    // Refresh data
    await initRequestsPage();
    
  } catch (error) {
    showToast('Error', error.message || 'Failed to move request', 'error');
  }
}

// Show move stage menu
function showMoveStageMenu(requestId, event) {
  event.stopPropagation();
  
  // Remove existing menu
  document.querySelectorAll('.stage-menu').forEach(m => m.remove());
  
  // Create menu
  const menu = document.createElement('div');
  menu.className = 'stage-menu dropdown-menu show';
  menu.style.cssText = `
    position: fixed;
    left: ${event.clientX}px;
    top: ${event.clientY}px;
    z-index: 1000;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    padding: 8px 0;
    min-width: 150px;
  `;
  
  menu.innerHTML = requestsState.stages.map(stage => `
    <button class="dropdown-item" style="
      display: flex;
      align-items: center;
      gap: 8px;
      width: 100%;
      padding: 8px 16px;
      border: none;
      background: none;
      cursor: pointer;
      text-align: left;
    " onclick="moveToStage(${requestId}, ${stage.id}); this.parentElement.remove();">
      <span style="width: 10px; height: 10px; border-radius: 50%; background: ${stage.color}"></span>
      ${stage.name}
    </button>
  `).join('');
  
  document.body.appendChild(menu);
  
  // Close menu on click outside
  setTimeout(() => {
    document.addEventListener('click', function closeMenu(e) {
      if (!menu.contains(e.target)) {
        menu.remove();
        document.removeEventListener('click', closeMenu);
      }
    });
  }, 10);
}

// Delete request
async function deleteRequest(id) {
  if (!confirm('Are you sure you want to delete this request?')) return;
  
  try {
    await GearGuardAPI.requests.delete(id);
    showToast('Success', 'Request deleted successfully', 'success');
    await initRequestsPage();
  } catch (error) {
    showToast('Error', error.message || 'Failed to delete request', 'error');
  }
}

// Equipment autofill
async function onEquipmentChange(equipmentId) {
  if (!equipmentId) return;
  
  try {
    const autofill = await GearGuardAPI.equipment.getAutofill(equipmentId);
    if (autofill) {
      // Auto-fill team if available
      if (autofill.default_team_id) {
        setFormValue('team-select', autofill.default_team_id);
      }
      // Could also auto-fill category, technician, etc.
    }
  } catch (error) {
    console.error('Autofill error:', error);
  }
}

// Close modal
function closeModal() {
  const modal = document.getElementById('request-modal');
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
  requestsState.currentRequest = null;
}

// Close panel
function closePanel() {
  const panel = document.getElementById('detail-panel');
  const overlay = document.getElementById('panel-overlay');
  if (panel) panel.classList.remove('active');
  if (overlay) overlay.classList.remove('active');
}

// Helper functions
function getPriorityClass(priority) {
  const classes = {
    'low': 'badge-secondary',
    'normal': 'badge-info',
    'high': 'badge-warning',
    'urgent': 'badge-danger'
  };
  return classes[priority] || 'badge-info';
}

function getPriorityIcon(priority) {
  const icons = {
    'low': 'arrow-down',
    'normal': 'minus',
    'high': 'arrow-up',
    'urgent': 'alert-triangle'
  };
  return icons[priority] || 'minus';
}

function capitalizeFirst(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function getInitials(name) {
  if (!name) return '??';
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
}

function truncate(str, length) {
  if (!str) return '';
  return str.length > length ? str.slice(0, length) + '...' : str;
}

function getLightColor(hex) {
  // Return a lighter version of the color
  return hex + '22';
}

function showLoading() {
  const grid = document.getElementById('request-grid');
  if (grid) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
        <div class="spinner" style="margin: 0 auto 16px;"></div>
        <p style="color: var(--text-muted);">Loading requests...</p>
      </div>
    `;
  }
}

function hideLoading() {
  // Loading hidden when content renders
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initRequestsPage);
