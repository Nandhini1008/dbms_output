// scripts.js

document.getElementById("search-form").onsubmit = function (e) {
    e.preventDefault();
    let name = document.getElementById("search-name").value;

    fetch(`/search_equipment?name=${name}`)
        .then(response => response.json())
        .then(data => {
            let resultDiv = document.getElementById("search-results");
            if (data === "NO Stock") {
                // If "NO Stock" is returned, show the message
                resultDiv.innerHTML = "<p>No equipment in stock.</p>";
            }
            else if (data.length > 0) {
                resultDiv.innerHTML = data.map(item => `
                    <p><strong>ID:</strong> ${item.equipment_id}, <strong>Name:</strong> ${item.name}, <strong>Quantity:</strong> ${item.quantity}</p>
                    <form action="/request_usage" method="POST">
                        <input type="hidden" name="equipment_id" value="${item.equipment_id}">
                        <input type="text" name="room_requested" placeholder="Room/Patient ID" required>
                        <button type="submit">Request Usage</button>
                    </form>
                    <hr>
                `).join("");
            } else {
                resultDiv.innerHTML = "<p>No equipment found.</p>";
            }
        })
        .catch(error => {
            console.error("Error fetching equipment:", error);
        });
};



document.getElementById("request-form").onsubmit = function (e) {
    e.preventDefault();
    let equipment_id = document.getElementById("request-equipment-id").value;
    let room_requested = document.getElementById("request-room").value;

    fetch('/request_use', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ equipment_id: equipment_id, room_requested: room_requested, requested_by: 1 })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("request-result").innerText = data.message;
    });
};

function requestEquipmentUse(equipmentId, roomRequested, requestedBy) {
    fetch('/request_use', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            equipment_id: equipmentId,
            room_requested: roomRequested,
            requested_by: requestedBy
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display confirmation message
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


document.getElementById("add-equipment-form").onsubmit = function (e) {
    e.preventDefault();
    let name = document.getElementById("equipment-name").value;
    let quantity = document.getElementById("equipment-quantity").value;
    let threshold = document.getElementById("equipment-threshold").value;
    let condition = document.getElementById("equipment-condition").value;

    fetch('/add_equipment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name, quantity: quantity, threshold: threshold, condition: condition })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("add-result").innerText = data.message;
    });
};
