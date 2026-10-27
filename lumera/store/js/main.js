/**
 * LUMERA COSMETICS — Main JavaScript
 * Handles: mobile menu, search toggle, navbar scroll effect,
 * category dropdown on mobile, and smooth interactions.
 * No external libraries required — pure vanilla JS.
 */
document.addEventListener('DOMContentLoaded', function () {

    // ── Elements ────────────────────────────────────────────
    const navbar = document.getElementById('navbar');
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navLinks = document.getElementById('navLinks');
    const searchToggle = document.getElementById('searchToggle');
    const searchBar = document.getElementById('searchBar');
    const searchClose = document.getElementById('searchClose');

    // ── Mobile Hamburger Menu ───────────────────────────────
    if (hamburgerBtn && navLinks) {
        hamburgerBtn.addEventListener('click', function () {
            this.classList.toggle('active');
            navLinks.classList.toggle('active');
            // Prevent body scroll when menu is open
            document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
        });

        // Close mobile menu when a link is clicked
        const links = navLinks.querySelectorAll('a:not(.dropdown-toggle)');
        links.forEach(function (link) {
            link.addEventListener('click', function () {
                hamburgerBtn.classList.remove('active');
                navLinks.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ── Mobile Category Dropdown Toggle ────────────────────
    // On mobile, the CSS hover doesn't work, so we use click
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function (e) {
            // Only prevent default on small screens
            if (window.innerWidth <= 768) {
                e.preventDefault();
                this.parentElement.classList.toggle('open');
            }
        });
    });

    // ── Search Bar Toggle ──────────────────────────────────
    if (searchToggle && searchBar) {
        searchToggle.addEventListener('click', function () {
            searchBar.classList.toggle('active');
            if (searchBar.classList.contains('active')) {
                // Focus the input after a brief delay for the animation
                setTimeout(function () {
                    searchBar.querySelector('input').focus();
                }, 100);
            }
        });
    }

    if (searchClose && searchBar) {
        searchClose.addEventListener('click', function () {
            searchBar.classList.remove('active');
        });
    }

    // Close search bar on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && searchBar && searchBar.classList.contains('active')) {
            searchBar.classList.remove('active');
        }
    });

    // ── Navbar Scroll Shadow ───────────────────────────────
    // Add a shadow to the navbar when the user scrolls down
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 10) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ── Auto-dismiss Messages ──────────────────────────────
    // Django success/error messages auto-hide after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert, index) {
        setTimeout(function () {
            if (alert.parentElement) {
                alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100%)';
                setTimeout(function () {
                    alert.remove();
                }, 400);
            }
        }, 5000 + (index * 500)); // Stagger the disappear times
    });

    // ── Smooth Scroll for Anchor Links ─────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ── Close mobile menu on window resize ─────────────────
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) {
            if (hamburgerBtn) hamburgerBtn.classList.remove('active');
            if (navLinks) navLinks.classList.remove('active');
            document.body.style.overflow = '';
            // Reset mobile dropdown states
            document.querySelectorAll('.nav-dropdown').forEach(function (dd) {
                dd.classList.remove('open');
            });
        }
    });

});