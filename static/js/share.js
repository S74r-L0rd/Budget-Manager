document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tabs
    var triggerTabList = [].slice.call(document.querySelectorAll('#sharingTabs button'))
    triggerTabList.forEach(function (triggerEl) {
        var tabTrigger = new bootstrap.Tab(triggerEl)
        triggerEl.addEventListener('click', function (event) {
            event.preventDefault()
            tabTrigger.show()
        })
    })

    // Function to load shared by me data
    function loadSharedByMe() {
        fetch('/api/shared-by-me')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('shared-by-me-list');
                tbody.innerHTML = '';
                data.forEach(item => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${item.sharedWith}</td>
                            <td>${item.type}</td>
                            <td>${item.itemName}</td>
                            <td>${new Date(item.sharedDate).toLocaleDateString()}</td>
                            <td>
                                <button class="btn btn-sm btn-danger" onclick="revokeAccess(${item.id})">
                                    Revoke Access
                                </button>
                            </td>
                        </tr>
                    `;
                });
            });
    }

    // Function to load shared with me data
    function loadSharedWithMe() {
        fetch('/api/shared-with-me')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('shared-with-me-list');
                tbody.innerHTML = '';
                data.forEach(item => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${item.sharedBy}</td>
                            <td>${item.type}</td>
                            <td>${item.itemName}</td>
                            <td>${new Date(item.sharedDate).toLocaleDateString()}</td>
                            <td>
                                <button class="btn btn-sm btn-primary" onclick="viewItem(${item.id})">
                                    View
                                </button>
                            </td>
                        </tr>
                    `;
                });
            });
    }

    // Load initial data
    loadSharedByMe();
    loadSharedWithMe();
});

// Function to revoke access
function revokeAccess(itemId) {
    if (confirm('Are you sure you want to revoke access?')) {
        fetch(`/api/revoke-access/${itemId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadSharedByMe();
            }
        });
    }
}

// Function to view shared item
function viewItem(itemId) {
    window.location.href = `/view-shared-item/${itemId}`;
}