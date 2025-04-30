// Image Slide Function for hero section
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.illustration');
    let index = 0;

    setInterval(() => {
        images.forEach((img, i) => {
            img.classList.toggle('active', i === index);
        });
        index = (index + 1) % images.length;
    }, 3000); // Change image every 3 seconds
});