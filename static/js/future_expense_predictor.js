export function scrollToPredictionWithOffset() {
  const OFFSET = 150;
  const target = document.querySelector('#prediction-result');

  if (target && target.offsetParent !== null) {
    // Section is visible in layout
    setTimeout(() => {
      const targetTop = target.getBoundingClientRect().top + window.scrollY - OFFSET;
      window.scrollTo({ top: targetTop, behavior: 'smooth' });
    }, 300);
  }
}

export function setupEditNoteModal() {
  const editModal = document.getElementById('editNoteModal');
  if (!editModal) return;

  editModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const shareId = button.getAttribute('data-share-id');
    const note = button.getAttribute('data-current-note');
    const currentUserId = button.getAttribute('data-current-user-id');

    document.getElementById('edit-share-id').value = shareId;
    document.getElementById('edit-note').value = note;

    // Set checked radio based on currentUserId
    const checkboxes = document.querySelectorAll('#edit-user-checkboxes input[type="radio"]');
    checkboxes.forEach(cb => {
      cb.checked = cb.value === currentUserId;
    });
  });
}

// Setup delete confirmation modal
export function setupDeleteModal() {
  const deleteModal = document.getElementById('deleteShareModal');
  const deleteForm = document.getElementById('deleteShareForm');

  if (!deleteModal || !deleteForm) return;

  deleteModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const shareId = button.getAttribute('data-share-id');
    deleteForm.action = `/delete-future-prediction-share/${shareId}`;
  });
}

function scrollToEditedCard() {
  const urlParams = new URLSearchParams(window.location.search);
  const editedId = urlParams.get('edited_share_id');
  if (editedId) {
    const target = document.getElementById(`shared-card-${editedId}`);
    if (target) {
      setTimeout(() => {
        const offset = 170;
        const targetTop = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: targetTop, behavior: 'smooth' });

        // Clean up URL to remove query parameter
        const newUrl = window.location.origin + window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
      }, 300);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  scrollToPredictionWithOffset();
  setupEditNoteModal();
  setupDeleteModal();
  scrollToEditedCard();
});