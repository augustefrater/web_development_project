// Run JavaScript only after the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {

    // Utility function to extract a named cookie (used for CSRF token)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCookie("csrftoken");
    console.log("CSRF Token:", csrfToken);

    // DOM references
    const machineSelect = document.getElementById("machine");
    const form = document.getElementById("fault-form");
    const result = document.getElementById("result");

    // Fetch machines assigned to the current logged-in user
    fetch("/api/assigned-machines/")
        .then(res => {
            if (!res.ok) {
                throw new Error("Not authenticated or error fetching assigned machines.");
            }
            return res.json();
        })
        .then(data => {
            console.log("Assigned machines:", data);

            // If user has no machines assigned
            if (!Array.isArray(data) || data.length === 0) {
                result.textContent = "⚠️ You have no machines assigned.";
                result.style.color = "orange";
                machineSelect.disabled = true; // Optional: disable dropdown if empty
                form.querySelector("button[type='submit']").disabled = true;
                return;
            }

            // Populate dropdown with machines
            data.forEach(machine => {
                const option = document.createElement("option");
                option.value = machine.machine_id;
                option.textContent = `${machine.name} (${machine.status})`;
                machineSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error("❌ Error fetching assigned machines:", error);
            result.textContent = "❌ Failed to load assigned machines. Are you logged in?";
            result.style.color = "red";
        });

    // Handle form submission via Fetch (AJAX)
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        console.log("Submitting fault report...");

        const payload = {
            machine: machineSelect.value,
            note: document.getElementById("note").value
        };

        console.log("Payload:", payload);

        try {
            const response = await fetch("/api/fault-cases/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                credentials: "same-origin",
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                result.textContent = "✅ Fault report submitted!";
                result.style.color = "green";
                form.reset();
            } else {
                const err = await response.json();
                result.textContent = "❌ Error: " + JSON.stringify(err);
                result.style.color = "red";
            }
        } catch (error) {
            result.textContent = "❌ Request failed: " + error;
            result.style.color = "red";
        }
    });
});