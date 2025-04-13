// Run JavaScript only after the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
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

    const machineSelect = document.getElementById("machine");
    const form = document.getElementById("faultForm");
    const result = document.getElementById("successMessage");
    const fileInput = document.getElementById("imageUpload");

    // Fetch machines assigned to the current logged-in user
    fetch("/api/assigned-machines/")
        .then(res => {
            if (!res.ok) throw new Error("Not authenticated or error fetching assigned machines.");
            return res.json();
        })
        .then(data => {
            if (!Array.isArray(data) || data.length === 0) {
                result.innerHTML = "⚠️ You have no machines assigned.";
                result.style.color = "orange";
                result.classList.add("active");
                machineSelect.disabled = true;
                form.querySelector("button[type='submit']").disabled = true;
                return;
            }

            data.forEach(machine => {
                const option = document.createElement("option");
                option.value = machine.machine_id;
                option.textContent = `${machine.name} (${machine.status})`;
                machineSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error("❌ Error fetching assigned machines:", error);
            result.innerHTML = "❌ Failed to load assigned machines. Are you logged in?";
            result.style.color = "red";
            result.classList.add("active");
        });

    // Handle form submission
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const note = document.getElementById("description").value;
        const machineId = machineSelect.value;
        const imageFile = fileInput.files[0];
        const newStatus = document.querySelector('input[name="machineStatus"]:checked').value;
        const reportedBy = document.getElementById("reportedBy").value;
        const faultPayload = { machine: machineId };

        try {
            const faultResponse = await fetch("/api/fault-cases/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                credentials: "same-origin",
                body: JSON.stringify(faultPayload)
            });

            if (!faultResponse.ok) {
                const err = await faultResponse.json();
                throw new Error("Fault report failed: " + JSON.stringify(err));
            }

            const faultData = await faultResponse.json();

            const noteResponse = await fetch("/api/fault-notes/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                credentials: "same-origin",
                body: JSON.stringify({
                    fault_case: faultData.id,
                    note_text: note
                })
            });

            if (!noteResponse.ok) {
                const err = await noteResponse.json();
                throw new Error("Creating fault note failed: " + JSON.stringify(err));
            }

            const noteData = await noteResponse.json();

            if (imageFile) {
                const formData = new FormData();
                formData.append("fault_note", noteData.id);
                formData.append("image", imageFile);

                const imageResponse = await fetch("/api/fault-note-images/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    credentials: "same-origin",
                    body: formData
                });

                if (!imageResponse.ok) {
                    const err = await imageResponse.json();
                    throw new Error("Image upload failed: " + JSON.stringify(err));
                }
            }

            // ✅ Update machine status
            await fetch(`/api/machines/${machineId}/`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                credentials: "same-origin",
                body: JSON.stringify({ status: newStatus })
            });

            result.textContent = "✅ Fault report submitted!";
            result.style.color = "#16a34a";
            result.classList.add("active");
            form.reset();
            document.getElementById("filePreview").classList.remove("active");
        } catch (error) {
            result.textContent = "❌ Error: " + error.message;
            result.style.color = "red";
            result.classList.add("active");
        }
    });
});
