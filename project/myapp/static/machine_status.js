document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/machines/")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("machine-status-list");
            container.innerHTML = "";

            data.forEach(machine => {
                const div = document.createElement("div");
                div.innerHTML = `<strong>${machine.name}</strong>: ${machine.status}`;
                container.appendChild(div);
            });
        })
        .catch(error => {
            console.error("Error fetching machine status:", error);
        });
});