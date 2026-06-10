// ── Desktop sidebar toggle ──────────────────────────────────────
const sidebarToggle = document.getElementById('sidebarToggle');
if (sidebarToggle) {
    if (localStorage.getItem('sidebarHidden') === '1') {
        document.body.classList.add('sidebar-hidden');
    }
    sidebarToggle.addEventListener('click', () => {
        document.body.classList.toggle('sidebar-hidden');
        localStorage.setItem(
            'sidebarHidden',
            document.body.classList.contains('sidebar-hidden') ? '1' : '0'
        );
    });
}

// ── Mobile hamburger toggle ─────────────────────────────────────
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu    = document.getElementById('mobileMenu');
const mobileOverlay = document.getElementById('mobileOverlay');

function closeMobileMenu() {
    if (mobileMenu)    mobileMenu.classList.remove('open');
    if (mobileOverlay) mobileOverlay.classList.remove('open');
}

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('open');
        mobileOverlay.classList.toggle('open');
    });
}

if (mobileOverlay) {
    mobileOverlay.addEventListener('click', closeMobileMenu);
}

document.querySelectorAll('.mobile-menu a:not([data-bs-toggle="collapse"])').forEach(link => {
    link.addEventListener('click', closeMobileMenu);
});
