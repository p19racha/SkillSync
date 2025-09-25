// Mobile menu toggle
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');

if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
}

// Hero CTA and other buttons
const heroCta = document.getElementById('hero-cta');
const finalCta = document.getElementById('final-cta');

if (heroCta) {
    heroCta.addEventListener('click', () => {
        window.location.href = 'auth.html#register';
    });
}

if (finalCta) {
    finalCta.addEventListener('click', () => {
        window.location.href = 'auth.html#register';
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
