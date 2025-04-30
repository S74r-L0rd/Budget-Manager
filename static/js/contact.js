// function to handle form submission
async function handleSubmit() {
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // validation
    if (!firstName || !lastName || !email || !message) {
        alert('Please fill in all fields');
        return;
    }

    if (!email.includes('@')) {
        alert('Please enter a valid email address');
        return;
    }

    try {
        const templateParams = {
            from_name: `${firstName} ${lastName}`,
            from_email: email,
            message: message
        };

        await emailjs.send(
            'service_l7alkef',
            'template_6aszau3',
            templateParams
        );

        // clear form
        document.getElementById('firstName').value = '';
        document.getElementById('lastName').value = '';
        document.getElementById('email').value = '';
        document.getElementById('message').value = '';

        alert('Message sent successfully!');
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to send message. Please try again.');
    }
}