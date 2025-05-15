document.addEventListener("DOMContentLoaded", function() {
    const participantsInput = document.getElementById("participants_hidden");
    const participantsEmailField = document.getElementById("participants_email");
    const addParticipantsBtn = document.getElementById("add-participants-btn");
    const participantEmails = document.getElementById("participant-emails");
    let participantsList = [];

    // Clear participants when the page loads (for editing)
    function clearParticipants() {
        participantsList = [];
        participantEmails.innerHTML = '<li class="list-group-item text-muted">No participants added yet.</li>';
        updateParticipantsInput();
    }

    // Initialize: Clear participants when editing
    if (window.location.href.includes("edit")) {
        clearParticipants();
    }

    // Add participant on button click
    addParticipantsBtn.addEventListener("click", function() {
        const email = participantsEmailField.value.trim();

        if (email && validateEmail(email) && !participantsList.includes(email)) {
            participantsList.push(email);
            addParticipantToList(email);
            updateParticipantsInput();
            participantsEmailField.value = "";
            participantsEmailField.focus();
        } else {
            alert("Invalid or duplicate email address.");
        }
    });

    // Function to add participant to the visual list
    function addParticipantToList(email) {
        // Remove unnecessary placeholder if it exists
        const placeholder = participantEmails.querySelector(".text-muted");
        if (placeholder) {
            placeholder.remove();
        }

        const listItem = document.createElement("li");
        listItem.className = "list-group-item d-flex justify-content-between align-items-center participant-item";
        listItem.setAttribute("data-email", email);
        listItem.innerHTML = `
            <span>${email}</span>
            <button type="button" class="btn btn-sm btn-outline-dark remove-participant" data-email="${email}">✖</button>
        `;
        participantEmails.appendChild(listItem);

        // Attach remove event
        listItem.querySelector(".remove-participant").addEventListener("click", function() {
            const removeEmail = this.getAttribute("data-email");
            participantsList = participantsList.filter(e => e !== removeEmail);
            updateParticipantsInput();
            listItem.remove();
            if (participantsList.length === 0) {
                showNoParticipantsMessage();
            }
        });
    }

    // Update the hidden input field with the latest participants
    function updateParticipantsInput() {
        participantsInput.value = participantsList.join(",");
    }

    // Show the "No participants added yet" message
    function showNoParticipantsMessage() {
        const noParticipants = document.createElement("li");
        noParticipants.className = "list-group-item text-muted";
        noParticipants.textContent = "No participants added yet.";
        participantEmails.appendChild(noParticipants);
    }

    // Email validation function
    function validateEmail(email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailPattern.test(email);
    }
});