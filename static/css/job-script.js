// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const sidebar = document.getElementById('sidebar');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(e) {
    if (window.innerWidth <= 1024) {
        if (sidebar && !sidebar.contains(e.target) && mobileMenuBtn && !mobileMenuBtn.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Calculate and update stats
function updateStats() {
    const rows = document.querySelectorAll('.job-row');
    const totalJobs = rows.length;
    let activeCount = 0;
    let pendingCount = 0;
    let companiesSet = new Set();

    rows.forEach(row => {
        const status = row.querySelector('.status-badge');
        if (status) {
            if (status.classList.contains('active')) activeCount++;
            if (status.classList.contains('pending')) pendingCount++;
        }
        
        const companyId = row.querySelector('.company-id');
        if (companyId) {
            companiesSet.add(companyId.textContent);
        }
    });

    document.getElementById('totalJobs').textContent = totalJobs;
    document.getElementById('activeJobs').textContent = activeCount;
    document.getElementById('pendingJobs').textContent = pendingCount;
    document.getElementById('totalCompanies').textContent = companiesSet.size;
    document.getElementById('totalRecords').textContent = totalJobs;
}

// Initialize stats on page load
document.addEventListener('DOMContentLoaded', updateStats);

// Search functionality
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('.job-row');
        
        rows.forEach(row => {
            const title = row.querySelector('.title')?.textContent.toLowerCase() || '';
            const description = row.querySelector('.description-cell')?.textContent.toLowerCase() || '';
            const company = row.querySelector('.company-name')?.textContent.toLowerCase() || '';
            
            const matches = title.includes(searchTerm) || 
                          description.includes(searchTerm) || 
                          company.includes(searchTerm);
            
            row.style.display = matches ? '' : 'none';
        });
        
        updateVisibleCount();
    });
}

// Status filter
const statusFilter = document.getElementById('statusFilter');
if (statusFilter) {
    statusFilter.addEventListener('change', function(e) {
        const filterValue = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('.job-row');
        
        rows.forEach(row => {
            if (!filterValue) {
                row.style.display = '';
            } else {
                const badge = row.querySelector('.status-badge');
                const matches = badge && badge.classList.contains(filterValue);
                row.style.display = matches ? '' : 'none';
            }
        });
        
        updateVisibleCount();
    });
}

// Sort functionality
const sortBy = document.getElementById('sortBy');
if (sortBy) {
    sortBy.addEventListener('change', function(e) {
        const tbody = document.getElementById('jobsTableBody');
        const rows = Array.from(tbody.querySelectorAll('.job-row'));
        
        rows.sort((a, b) => {
            switch(e.target.value) {
                case 'title':
                    const titleA = a.querySelector('.title').textContent;
                    const titleB = b.querySelector('.title').textContent;
                    return titleA.localeCompare(titleB);
                    
                case 'company':
                    const companyA = a.querySelector('.company-name').textContent;
                    const companyB = b.querySelector('.company-name').textContent;
                    return companyA.localeCompare(companyB);
                    
                case 'recent':
                default:
                    // Keep original order for "most recent"
                    return 0;
            }
        });
        
        rows.forEach(row => tbody.appendChild(row));
    });
}

// Update visible count
function updateVisibleCount() {
    const visibleRows = document.querySelectorAll('.job-row:not([style*="display: none"])');
    document.getElementById('showingEnd').textContent = visibleRows.length;
}

// Select all checkbox
const selectAll = document.getElementById('selectAll');
if (selectAll) {
    selectAll.addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('.row-checkbox');
        checkboxes.forEach(cb => cb.checked = this.checked);
    });
}

// View toggle
const viewButtons = document.querySelectorAll('.view-btn');
viewButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        viewButtons.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        const view = this.dataset.view;
        // Add grid view implementation here if needed
        console.log('Switched to:', view, 'view');
    });
});

// View job details
function viewJob(jobId) {
    const modal = document.getElementById('jobModal');
    const modalBody = document.getElementById('modalBody');
    
    // Find the job row
    const row = document.querySelector(`[data-job-id="${jobId}"]`);
    if (row) {
        const title = row.querySelector('.title').textContent;
        const description = row.querySelector('.description-cell').textContent;
        const company = row.querySelector('.company-name').textContent;
        const status = row.querySelector('.status-badge').textContent;
        const posted = row.querySelector('.posted-date').textContent;
        
        modalBody.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div>
                    <div style="color: var(--gray); font-size: 0.875rem; margin-bottom: 0.5rem;">Job ID</div>
                    <div style="font-weight: 600;">#${jobId}</div>
                </div>
                <div>
                    <div style="color: var(--gray); font-size: 0.875rem; margin-bottom: 0.5rem;">Job Title</div>
                    <div style="font-size: 1.25rem; font-weight: 700; color: var(--dark);">${title}</div>
                </div>
                <div>
                    <div style="color: var(--gray); font-size: 0.875rem; margin-bottom: 0.5rem;">Description</div>
                    <div style="color: var(--dark); line-height: 1.7;">${description}</div>
                </div>
                <div>
                    <div style="color: var(--gray); font-size: 0.875rem; margin-bottom: 0.5rem;">Company</div>
                    <div style="font-weight: 600;">${company}</div>
                </div>
                <div style="display: flex; gap: 2rem;">
                    <div>
                        <div style="color: var(--gray); font-size: 0.875rem; margin-bottom: 0.5rem;">Status</div>
                        <div><span class="status-badge ${status.toLowerCase()}">${status}</span></div>
                    </div>
                    <div>
                        <div style="color: var(--gray); font-size: 0.875rem; margin-bottom: 0.5rem;">Posted</div>
                        <div style="color: var(--dark);">${posted}</div>
                    </div>
                </div>
            </div>
        `;
    }
    
    modal.classList.add('active');
}

// Edit job
function editJob(jobId) {
    showNotification(`Editing job #${jobId}`, 'success');
    // Add your edit logic here
}

// Delete job
function deleteJob(jobId) {
    if (confirm('Are you sure you want to delete this job?')) {
        const row = document.querySelector(`[data-job-id="${jobId}"]`);
        if (row) {
            row.style.animation = 'slideOut 0.3s ease forwards';
            
            setTimeout(() => {
                row.remove();
                showNotification('Job deleted successfully', 'success');
                updateStats();
                updateVisibleCount();
            }, 300);
        }
    }
}

// Close modal
function closeModal() {
    const modal = document.getElementById('jobModal');
    modal.classList.remove('active');
}

// Edit from modal
function editFromModal() {
    closeModal();
    showNotification('Edit functionality coming soon!', 'success');
}

// Export data
function exportData() {
    showNotification('Exporting data...', 'success');
    // Add your export logic here
}

// Add new job
function addNewJob() {
    showNotification('Add job functionality coming soon!', 'success');
    // Add your create job logic here
}

// Show notification
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    const modal = document.getElementById('jobModal');
    if (e.target === modal) {
        closeModal();
    }
});

// Pagination
const pageButtons = document.querySelectorAll('.page-btn');
pageButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        if (this.id !== 'prevBtn' && this.id !== 'nextBtn' && this.textContent !== '...') {
            pageButtons.forEach(b => {
                if (b.id !== 'prevBtn' && b.id !== 'nextBtn') {
                    b.classList.remove('active');
                }
            });
            this.classList.add('active');
        }
    });
});