// ─── Sidebar Toggle ───────────────────────────────────────────────────────────
const sidebar       = document.getElementById('sidebar');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const sidebarToggle = document.getElementById('sidebarToggle');

if (mobileMenuBtn && sidebar) {
    mobileMenuBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        sidebar.classList.toggle('active');
    });
}

if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function (e) {
        e.stopPropagation();
        sidebar.classList.remove('active');
    });
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function (e) {
    if (window.innerWidth <= 1024 && sidebar) {
        const clickedOutside =
            !sidebar.contains(e.target) &&
            !(mobileMenuBtn && mobileMenuBtn.contains(e.target));
        if (clickedOutside) {
            sidebar.classList.remove('active');
        }
    }
});

// ─── Active Nav Item ──────────────────────────────────────────────────────────
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function () {
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        this.classList.add('active');
    });
});

// ─── Approve / Reject ─────────────────────────────────────────────────────────
document.querySelectorAll('.btn-approve').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        const item = this.closest('.pending-item');
        const name = item.querySelector('.pending-name').textContent;
        item.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => { item.remove(); showNotification(`${name} approved!`, 'success'); updatePendingCount(-1); }, 300);
    });
});

document.querySelectorAll('.btn-reject').forEach(btn => {
    btn.addEventListener('click', function (e) {
        e.preventDefault();
        const item = this.closest('.pending-item');
        const name = item.querySelector('.pending-name').textContent;
        item.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => { item.remove(); showNotification(`${name} rejected!`, 'error'); updatePendingCount(-1); }, 300);
    });
});

function updatePendingCount(change) {
    document.querySelectorAll('.nav-item .badge, .count-badge').forEach(badge => {
        const n = parseInt(badge.textContent) + change;
        badge.textContent = n;
        badge.style.display = n <= 0 ? 'none' : '';
    });
}

// ─── Toast Notification ───────────────────────────────────────────────────────
function showNotification(message, type) {
    const el = document.createElement('div');
    el.textContent = message;
    el.style.cssText = `
        position:fixed; top:2rem; right:2rem; z-index:10000;
        background:${type === 'success' ? '#10b981' : '#ef4444'};
        color:#fff; padding:1rem 1.5rem; border-radius:.5rem;
        box-shadow:0 4px 12px rgba(0,0,0,.2);
        animation:slideInRight .3s ease;
    `;
    document.body.appendChild(el);
    setTimeout(() => { el.style.animation = 'slideOutRight .3s ease'; setTimeout(() => el.remove(), 300); }, 3000);
}

// ─── Keyframes ────────────────────────────────────────────────────────────────
const kf = document.createElement('style');
kf.textContent = `
    @keyframes slideOut      { to { opacity:0; transform:translateX(100%); } }
    @keyframes slideInRight  { from { opacity:0; transform:translateX(100%); } to { opacity:1; transform:translateX(0); } }
    @keyframes slideOutRight { to   { opacity:0; transform:translateX(100%); } }
`;
document.head.appendChild(kf);

// ─── Search ───────────────────────────────────────────────────────────────────
const searchInput = document.querySelector('.search-box input');
if (searchInput) {
    searchInput.addEventListener('input', e => console.log('Search:', e.target.value));
}

// ─── Notification Button ──────────────────────────────────────────────────────
const notifBtn = document.querySelector('.notification-btn');
if (notifBtn) notifBtn.addEventListener('click', () => showNotification('You have 5 new notifications', 'success'));

// ─── Scroll Animations ────────────────────────────────────────────────────────
const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.style.animation = 'fadeIn .5s ease forwards'; });
}, { threshold: 0.1 });
document.querySelectorAll('.stat-card, .card, .quick-card').forEach(el => observer.observe(el));

// ─── Simulated Real-time Stats ────────────────────────────────────────────────
setInterval(() => {
    document.querySelectorAll('.stat-value').forEach((v, i) => {
        if (i !== 1) {
            const n = parseInt(v.textContent.replace(/,/g, '')) + Math.floor(Math.random() * 10 - 5);
            v.textContent = n.toLocaleString();
        }
    });
}, 10000);