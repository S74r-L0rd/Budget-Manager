document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling function
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

    // Event listener for buttons with data-target attribute
    document.querySelectorAll('button[data-target]').forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            console.log('Button clicked, target ID:', targetId); // Debug log
            scrollToElementSmoothly(targetId);
        });
    });

    // Form submission handler
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleSubmit);
    }

    // EmailJS form submission handler
    function handleSubmit(event) {
        event.preventDefault();
        
        // Collect form data
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        // Prepare template parameters
        const templateParams = {
            from_name: `${firstName} ${lastName}`,
            from_email: email,
            message: message
        };

        // Send email using EmailJS
        emailjs.send('service_l7alkef', 'template_6aszau3', templateParams)
            .then(() => {
                alert('Message sent successfully!');
                contactForm.reset(); // Clear form after successful submission
            }, (error) => {
                console.error('Email send failed:', error);
                alert('Failed to send message. Please try again.');
            });
    }
});
