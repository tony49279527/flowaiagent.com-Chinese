// Hamburger Menu Toggle
document.addEventListener('DOMContentLoaded', function () {
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');

    if (hamburgerBtn && mobileMenuOverlay) {
        hamburgerBtn.addEventListener('click', function () {
            hamburgerBtn.classList.toggle('active');
            mobileMenuOverlay.classList.toggle('active');
            document.body.style.overflow = mobileMenuOverlay.classList.contains('active') ? 'hidden' : '';
            hamburgerBtn.setAttribute('aria-expanded', mobileMenuOverlay.classList.contains('active'));
        });

        // Close menu when clicking a link
        mobileMenuOverlay.querySelectorAll('.mobile-nav-link').forEach(link => {
            link.addEventListener('click', function () {
                hamburgerBtn.classList.remove('active');
                mobileMenuOverlay.classList.remove('active');
                document.body.style.overflow = '';
            });
        });

        // Close menu when clicking outside
        mobileMenuOverlay.addEventListener('click', function (e) {
            if (e.target === mobileMenuOverlay) {
                hamburgerBtn.classList.remove('active');
                mobileMenuOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
});
