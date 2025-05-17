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

    // Drag-to-scroll for product-card-scroll
    const scrollContainer = document.querySelector('.product-card-scroll');

    if (scrollContainer) {
        let isDown = false;
        let startX;
        let scrollLeft;

        scrollContainer.addEventListener('mousedown', (e) => {
            isDown = true;
            scrollContainer.classList.add('dragging');
            startX = e.pageX - scrollContainer.offsetLeft;
            scrollLeft = scrollContainer.scrollLeft;
        });

        scrollContainer.addEventListener('mouseleave', () => {
            isDown = false;
            scrollContainer.classList.remove('dragging');
        });

        scrollContainer.addEventListener('mouseup', () => {
            isDown = false;
            scrollContainer.classList.remove('dragging');
        });

        scrollContainer.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - scrollContainer.offsetLeft;
            const walk = (x - startX) * 1.5;
            scrollContainer.scrollLeft = scrollLeft - walk;
        });
    }
});