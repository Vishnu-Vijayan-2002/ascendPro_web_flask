// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const sidebar = document.getElementById('sidebar');

mobileMenuBtn.addEventListener('click', function() {
    sidebar.classList.toggle('active');
});

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(e) {
    if (window.innerWidth <= 1024) {
        if (!sidebar.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Active nav item
const navItems = document.querySelectorAll('.nav-item');
navItems.forEach(item => {
    item.addEventListener('click', function() {
        navItems.forEach(nav => nav.classList.remove('active'));
        this.classList.add('active');
    });
});

// Approve/Reject functionality
const approveButtons = document.querySelectorAll('.btn-approve');
const rejectButtons = document.querySelectorAll('.btn-reject');

approveButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const pendingItem = this.closest('.pending-item');
        const name = pendingItem.querySelector('.pending-name').textContent;
        
        // Add animation
        pendingItem.style.animation = 'slideOut 0.3s ease forwards';
        
        setTimeout(() => {
            pendingItem.remove();
            showNotification(`${name} has been approved!`, 'success');
            updatePendingCount(-1);
        }, 300);
    });
});

rejectButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const pendingItem = this.closest('.pending-item');
        const name = pendingItem.querySelector('.pending-name').textContent;
        
        // Add animation
        pendingItem.style.animation = 'slideOut 0.3s ease forwards';
        
        setTimeout(() => {
            pendingItem.remove();
            showNotification(`${name} has been rejected!`, 'error');
            updatePendingCount(-1);
        }, 300);
    });
});

// Update pending count
function updatePendingCount(change) {
    const badges = document.querySelectorAll('.nav-item .badge, .count-badge');
    badges.forEach(badge => {
        const currentCount = parseInt(badge.textContent);
        const newCount = currentCount + change;
        badge.textContent = newCount;
        
        if (newCount === 0) {
            badge.style.display = 'none';
        }
    });
}

// Show notification
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add styles
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

// Search functionality
const searchInput = document.querySelector('.search-box input');
searchInput.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    console.log('Searching for:', searchTerm);
    // Add your search logic here
});

// Notification button
const notificationBtn = document.querySelector('.notification-btn');
notificationBtn.addEventListener('click', function() {
    showNotification('You have 5 new notifications', 'success');
});

// Quick action buttons
const actionButtons = document.querySelectorAll('.action-btn');
actionButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        const action = this.textContent.trim();
        showNotification(`${action} functionality coming soon!`, 'success');
    });
});

// Stat cards animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeIn 0.5s ease forwards';
        }
    });
}, observerOptions);

document.querySelectorAll('.stat-card, .card, .quick-card').forEach(el => {
    observer.observe(el);
});

// Simulated real-time updates
setInterval(() => {
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach((value, index) => {
        if (index !== 1) { // Don't update pending count
            const currentValue = parseInt(value.textContent.replace(/,/g, ''));
            const change = Math.floor(Math.random() * 10) - 5;
            const newValue = currentValue + change;
            value.textContent = newValue.toLocaleString();
        }
    });
}, 10000); // Update every 10 seconds