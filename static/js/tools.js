document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".fade-in-up");
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("animate__animated", "animate__fadeInUp");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));

    // Smooth scrolling functionality
    function scrollToElementSmoothly(id, offset = 150, duration = 600) {
        const target = document.getElementById(id);
        if (!target) return;
        
        const targetY = target.getBoundingClientRect().top + window.pageYOffset - offset;
        const startY = window.scrollY;
        const distance = targetY - startY;
        let startTime = null;
        
        function easeInOutQuad(t) {
            return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
        }
        
        function animateScroll(currentTime) {
            if (!startTime) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const progress = easeInOutQuad(Math.min(timeElapsed / duration, 1));
            window.scrollTo(0, startY + distance * progress);
            
            if (timeElapsed < duration) {
                requestAnimationFrame(animateScroll);
            }
        }
        
        requestAnimationFrame(animateScroll);
    }

    document.querySelectorAll('a[href*="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                scrollToElementSmoothly(targetId);
            }
        });
    });

    window.addEventListener('load', () => {
        if (window.location.hash) {
            const targetId = window.location.hash.substring(1);
            setTimeout(() => {
                scrollToElementSmoothly(targetId);
            }, 100);
        }
    });
});