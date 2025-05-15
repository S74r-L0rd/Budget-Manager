document.addEventListener("DOMContentLoaded", function() {
    let participantsList = [];
    const participantsInput = document.getElementById("participants_hidden");
    const participantEmails = document.getElementById("participant-emails");
    const addParticipantsBtn = document.getElementById("add-participants-btn");
    const participantsField = document.getElementById("participants");

    // Clear participants list on page load (edit mode)
    participantsList = [];
    participantEmails.innerHTML = '<li class="list-group-item text-muted">No participants added yet.</li>';

    // Add participant on button click
    addParticipantsBtn.addEventListener("click", function() {
        const email = participantsField.value.trim();
        if (email && !participantsList.includes(email)) {
            participantsList.push(email);
            addParticipantToList(email);
            updateParticipants();
            participantsField.value = "";
        }
    });

    // Function to add a participant to the visible list
    function addParticipantToList(email) {
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
            updateParticipants();
            listItem.remove();
        });
    }

    // Update the hidden input field with the latest participants
    function updateParticipants() {
        participantsInput.value = participantsList.join(",");
    }

    // Ensure input is up-to-date on submit
    document.querySelector("form").addEventListener("submit", function() {
        updateParticipants();
    });
});
