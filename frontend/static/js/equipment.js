/**
 * GearGuard Equipment Page JavaScript
 * Handles equipment list, CRUD operations, and filtering
 */

// State management
let allEquipment = [];
let categories = [];
let teams = [];
let editingEquipmentId = null;

/**
 * Initialize the equipment page
 */
document.addEventListener('DOMContentLoaded', function() {
    initEquipmentPage();
});

async function initEquipmentPage() {
    try {
        // Load all data in parallel
        const [equipmentData, categoriesData, teamsData] = await Promise.all([
            GearGuardAPI.equipment.getAll(),
            GearGuardAPI.categories.getAll(),
            GearGuardAPI.teams.getAll()
        ]);
        
        allEquipment = equipmentData.equipment || equipmentData || [];
        categories = categoriesData.categories || categoriesData || [];
        teams = teamsData.teams || teamsData || [];
        
        // Populate filter dropdowns
        populateCategoryFilter();
        populateTeamDropdown();
        
        // Update stats
        updateStats();
        
        // Render equipment
        renderEquipment(allEquipment);
        
        // Reinitialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    } catch (error) {
        console.error('Failed to initialize equipment page:', error);
        document.getElementById('equipment-grid').innerHTML = `
            <div class="loading-placeholder">
                <i data-lucide="alert-circle" style="width: 32px; height: 32px; color: var(--danger);"></i>
                <p>Failed to load equipment. Please refresh the page.</p>
            </div>
        `;
    }
}

/**
 * Populate category filter dropdown
 */
function populateCategoryFilter() {
    const filterSelect = document.getElementById('filter-category');
    filterSelect.innerHTML = '<option value="">All Categories</option>';
    
    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.name;
        filterSelect.appendChild(option);
    });
    
    // Also populate the form dropdown
    const formSelect = document.getElementById('equipment-category');
    if (formSelect) {
        formSelect.innerHTML = '<option value="">Select category</option>';
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = cat.name;
            formSelect.appendChild(option);
        });
    }
}

/**
 * Populate team dropdown in form
 */
function populateTeamDropdown() {
    const formSelect = document.getElementById('equipment-team');
    if (formSelect) {
        formSelect.innerHTML = '<option value="">Select team</option>';
        teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team.id;
            option.textContent = team.name;
            formSelect.appendChild(option);
        });
    }
}

/**
 * Update statistics
 */
function updateStats() {
    const total = allEquipment.length;
    const operational = allEquipment.filter(e => e.status === 'operational').length;
    const maintenance = allEquipment.filter(e => e.status === 'maintenance').length;
    const broken = allEquipment.filter(e => e.status === 'broken').length;
    
    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-operational').textContent = operational;
    document.getElementById('stat-maintenance').textContent = maintenance;
    document.getElementById('stat-broken').textContent = broken;
}

/**
 * Render equipment cards
 */
function renderEquipment(equipment) {
    const grid = document.getElementById('equipment-grid');
    
    if (!equipment || equipment.length === 0) {
        grid.innerHTML = `
            <div class="loading-placeholder">
                <i data-lucide="package" style="width: 48px; height: 48px; color: var(--text-muted);"></i>
                <p>No equipment found</p>
                <button class="btn btn-primary" onclick="openCreateModal()">
                    <i data-lucide="plus" style="width: 16px; height: 16px;"></i>
                    Add Equipment
                </button>
            </div>
        `;
        if (typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }
    
    grid.innerHTML = equipment.map(eq => createEquipmentCard(eq)).join('');
    
    // Reinitialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

/**
 * Create equipment card HTML
 */
function createEquipmentCard(equipment) {
    const statusClass = equipment.status || 'operational';
    const statusLabel = getStatusLabel(equipment.status);
    const categoryName = getCategoryName(equipment.category_id);
    const teamName = getTeamName(equipment.default_team_id);
    
    const formatCurrency = (value) => {
        if (!value) return '-';
        return '₹' + parseFloat(value).toLocaleString('en-IN');
    };
    
    const formatDate = (dateStr) => {
        if (!dateStr) return '-';
        return new Date(dateStr).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };
    
    return `
        <div class="equipment-card" data-id="${equipment.id}">
            <div class="equipment-card-header">
                <div>
                    <span class="equipment-code">${equipment.code || 'N/A'}</span>
                    <h3 class="equipment-name">${equipment.name}</h3>
                    <div class="equipment-category">
                        <i data-lucide="folder" style="width: 14px; height: 14px;"></i>
                        ${categoryName}
                    </div>
                </div>
                <span class="equipment-status ${statusClass}">${statusLabel}</span>
            </div>
            
            <div class="equipment-details">
                <div class="detail-item">
                    <span class="detail-label">Model</span>
                    <span class="detail-value">${equipment.model || '-'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Manufacturer</span>
                    <span class="detail-value">${equipment.manufacturer || '-'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Location</span>
                    <span class="detail-value">${equipment.location || '-'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Department</span>
                    <span class="detail-value">${equipment.department || '-'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Cost</span>
                    <span class="detail-value">${formatCurrency(equipment.cost)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Team</span>
                    <span class="detail-value">${teamName}</span>
                </div>
            </div>
            
            <div class="equipment-actions">
                <button class="btn btn-secondary" onclick="editEquipment(${equipment.id})" title="Edit">
                    <i data-lucide="edit-2" style="width: 14px; height: 14px;"></i>
                    Edit
                </button>
                <button class="btn btn-secondary" onclick="createRequestForEquipment(${equipment.id})" title="Create Request">
                    <i data-lucide="wrench" style="width: 14px; height: 14px;"></i>
                    Request
                </button>
                <button class="btn btn-danger" onclick="deleteEquipment(${equipment.id})" title="Delete">
                    <i data-lucide="trash-2" style="width: 14px; height: 14px;"></i>
                </button>
            </div>
        </div>
    `;
}

/**
 * Get status label
 */
function getStatusLabel(status) {
    const labels = {
        'operational': 'Operational',
        'maintenance': 'Maintenance',
        'broken': 'Broken'
    };
    return labels[status] || status || 'Unknown';
}

/**
 * Get category name by ID
 */
function getCategoryName(categoryId) {
    if (!categoryId) return 'Uncategorized';
    const category = categories.find(c => c.id === categoryId);
    return category ? category.name : 'Unknown';
}

/**
 * Get team name by ID
 */
function getTeamName(teamId) {
    if (!teamId) return '-';
    const team = teams.find(t => t.id === teamId);
    return team ? team.name : 'Unknown';
}

/**
 * Filter equipment based on search and filters
 */
function filterEquipment() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const categoryFilter = document.getElementById('filter-category').value;
    const statusFilter = document.getElementById('filter-status').value;
    
    let filtered = allEquipment;
    
    // Search filter
    if (searchTerm) {
        filtered = filtered.filter(eq => 
            (eq.name && eq.name.toLowerCase().includes(searchTerm)) ||
            (eq.code && eq.code.toLowerCase().includes(searchTerm)) ||
            (eq.model && eq.model.toLowerCase().includes(searchTerm)) ||
            (eq.manufacturer && eq.manufacturer.toLowerCase().includes(searchTerm)) ||
            (eq.location && eq.location.toLowerCase().includes(searchTerm))
        );
    }
    
    // Category filter
    if (categoryFilter) {
        filtered = filtered.filter(eq => eq.category_id == categoryFilter);
    }
    
    // Status filter
    if (statusFilter) {
        filtered = filtered.filter(eq => eq.status === statusFilter);
    }
    
    renderEquipment(filtered);
}

/**
 * Open create modal
 */
function openCreateModal() {
    editingEquipmentId = null;
    document.getElementById('modal-title').textContent = 'Add Equipment';
    document.getElementById('submit-btn-text').textContent = 'Create Equipment';
    document.getElementById('equipment-form').reset();
    document.getElementById('equipment-id').value = '';
    
    // Generate next equipment code
    const maxCode = allEquipment.reduce((max, eq) => {
        if (eq.code) {
            const num = parseInt(eq.code.replace('EQ-', ''));
            return num > max ? num : max;
        }
        return max;
    }, 0);
    document.getElementById('equipment-code').value = `EQ-${String(maxCode + 1).padStart(4, '0')}`;
    
    document.getElementById('equipment-modal').classList.add('active');
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

/**
 * Edit equipment
 */
async function editEquipment(id) {
    editingEquipmentId = id;
    const equipment = allEquipment.find(e => e.id === id);
    
    if (!equipment) {
        alert('Equipment not found');
        return;
    }
    
    document.getElementById('modal-title').textContent = 'Edit Equipment';
    document.getElementById('submit-btn-text').textContent = 'Save Changes';
    document.getElementById('equipment-id').value = equipment.id;
    document.getElementById('equipment-code').value = equipment.code || '';
    document.getElementById('equipment-name').value = equipment.name || '';
    document.getElementById('equipment-category').value = equipment.category_id || '';
    document.getElementById('equipment-status').value = equipment.status || 'operational';
    document.getElementById('equipment-model').value = equipment.model || '';
    document.getElementById('equipment-manufacturer').value = equipment.manufacturer || '';
    document.getElementById('equipment-location').value = equipment.location || '';
    document.getElementById('equipment-department').value = equipment.department || '';
    document.getElementById('equipment-team').value = equipment.default_team_id || '';
    document.getElementById('equipment-cost').value = equipment.cost || '';
    document.getElementById('equipment-purchase-date').value = equipment.purchase_date || '';
    document.getElementById('equipment-warranty').value = equipment.warranty_expiry || '';
    document.getElementById('equipment-owner').value = equipment.owner_name || '';
    document.getElementById('equipment-notes').value = equipment.notes || '';
    
    document.getElementById('equipment-modal').classList.add('active');
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

/**
 * Close modal
 */
function closeModal() {
    document.getElementById('equipment-modal').classList.remove('active');
    editingEquipmentId = null;
}

/**
 * Submit equipment form
 */
async function submitEquipment(event) {
    event.preventDefault();
    
    const formData = {
        code: document.getElementById('equipment-code').value,
        name: document.getElementById('equipment-name').value,
        category_id: parseInt(document.getElementById('equipment-category').value) || null,
        status: document.getElementById('equipment-status').value,
        model: document.getElementById('equipment-model').value || null,
        manufacturer: document.getElementById('equipment-manufacturer').value || null,
        location: document.getElementById('equipment-location').value || null,
        department: document.getElementById('equipment-department').value || null,
        default_team_id: parseInt(document.getElementById('equipment-team').value) || null,
        cost: parseFloat(document.getElementById('equipment-cost').value) || null,
        purchase_date: document.getElementById('equipment-purchase-date').value || null,
        warranty_expiry: document.getElementById('equipment-warranty').value || null,
        owner_name: document.getElementById('equipment-owner').value || null,
        notes: document.getElementById('equipment-notes').value || null
    };
    
    try {
        if (editingEquipmentId) {
            // Update existing
            await GearGuardAPI.equipment.update(editingEquipmentId, formData);
            showNotification('Equipment updated successfully', 'success');
        } else {
            // Create new
            await GearGuardAPI.equipment.create(formData);
            showNotification('Equipment created successfully', 'success');
        }
        
        closeModal();
        await initEquipmentPage(); // Refresh data
    } catch (error) {
        console.error('Failed to save equipment:', error);
        showNotification('Failed to save equipment: ' + error.message, 'error');
    }
}

/**
 * Delete equipment
 */
async function deleteEquipment(id) {
    const equipment = allEquipment.find(e => e.id === id);
    if (!confirm(`Are you sure you want to delete "${equipment?.name}"?`)) {
        return;
    }
    
    try {
        await GearGuardAPI.equipment.delete(id);
        showNotification('Equipment deleted successfully', 'success');
        await initEquipmentPage(); // Refresh data
    } catch (error) {
        console.error('Failed to delete equipment:', error);
        showNotification('Failed to delete equipment: ' + error.message, 'error');
    }
}

/**
 * Create maintenance request for equipment
 */
function createRequestForEquipment(equipmentId) {
    window.location.href = `/requests?action=create&equipment_id=${equipmentId}`;
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i data-lucide="${type === 'success' ? 'check-circle' : type === 'error' ? 'alert-circle' : 'info'}" style="width: 18px; height: 18px;"></i>
        <span>${message}</span>
    `;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'var(--success)' : type === 'error' ? 'var(--danger)' : 'var(--primary)'};
        color: white;
        padding: 12px 20px;
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    if (typeof lucide !== 'undefined') lucide.createIcons();
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Close modal when clicking on overlay background
document.addEventListener('click', function(event) {
    const modal = document.getElementById('equipment-modal');
    if (modal && modal.classList.contains('active') && event.target === modal) {
        closeModal();
    }
});

// Close modal on escape key
document.addEventListener('keydown', function(event) {
    const modal = document.getElementById('equipment-modal');
    if (event.key === 'Escape' && modal && modal.classList.contains('active')) {
        closeModal();
    }
});
