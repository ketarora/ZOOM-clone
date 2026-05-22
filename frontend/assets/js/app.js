/**
 * ZoomConnect Application Logic
 * Provides lightweight interactions to simulate a SPA-like experience and add UI polish.
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initClock();
    initAutoExpandTextarea();
    initMeetingTimer();
    initSidebarToggle();
});

function initNavigation() {
    // Determine current page to set active state in sidebar
    const path = window.location.pathname;
    const page = path.split('/').pop() || 'dashboard.html';

    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('data-page') === page) {
            link.classList.add('bg-primary/10', 'text-primary', 'font-semibold');
            link.classList.remove('text-on-surface', 'hover:bg-surface-container-high');
        }
    });

    // Add slight fade in for SPA feel
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.2s ease-in-out';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 50);
}

function initClock() {
    const clockElements = document.querySelectorAll('.live-clock');
    if (clockElements.length === 0) return;

    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const dateString = now.toLocaleDateString([], { weekday: 'long', month: 'short', day: 'numeric' });

        clockElements.forEach(el => {
            el.innerHTML = `<div class="text-4xl font-light">${timeString}</div><div class="text-sm text-secondary mt-1">${dateString}</div>`;
        });
    }

    updateClock();
    setInterval(updateClock, 1000 * 60); // Update every minute
}

function initAutoExpandTextarea() {
    const textareas = document.querySelectorAll('.auto-expand');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
            // Limit max height
            if (this.scrollHeight > 150) {
                this.style.overflowY = 'auto';
                this.style.height = '150px';
            } else {
                this.style.overflowY = 'hidden';
            }
        });
    });
}

function initMeetingTimer() {
    const timerElement = document.querySelector('.meeting-timer');
    if (!timerElement) return;

    let seconds = 0;
    setInterval(() => {
        seconds++;
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;

        const formatted = [
            hrs > 0 ? hrs.toString().padStart(2, '0') : null,
            mins.toString().padStart(2, '0'),
            secs.toString().padStart(2, '0')
        ].filter(Boolean).join(':');

        timerElement.textContent = formatted;
    }, 1000);
}

function initSidebarToggle() {
    const toggleBtns = document.querySelectorAll('button:has(.material-symbols-outlined:contains("menu"))');
    const sidebar = document.querySelector('nav');

    if (!sidebar) return;

    // In a real implementation this would slide the sidebar out on mobile.
    // We'll just do a basic toggle for now if requested.
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (sidebar.classList.contains('hidden')) {
                sidebar.classList.remove('hidden');
                sidebar.classList.add('flex', 'absolute', 'z-50', 'w-64', 'shadow-lg');
            } else {
                sidebar.classList.add('hidden');
                sidebar.classList.remove('flex', 'absolute', 'z-50', 'w-64', 'shadow-lg');
            }
        });
    });
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 px-4 py-2 rounded shadow-lg transition-opacity duration-300 z-50 text-white ${type === 'success' ? 'bg-success' : 'bg-primary'}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Make showToast globally available
window.showToast = showToast;

// Add copy link listener globally for elements with data-copy attribute
document.addEventListener('DOMContentLoaded', () => {
    const copyBtns = document.querySelectorAll('[data-copy]');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const textToCopy = btn.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                showToast('Link copied to clipboard!', 'success');
            }).catch(err => {
                showToast('Failed to copy', 'error');
            });
        });
    });
});
