// Function to preview image at the account setting page
function previewImage(event) {
    const image = document.getElementById('profile-img');
    image.src = URL.createObjectURL(event.target.files[0]);
  }
