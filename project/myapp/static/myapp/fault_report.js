// ✅ Wait until the full HTML document is loaded before executing the JavaScript code
document.addEventListener("DOMContentLoaded", () => {

    // 🔐 Get the CSRF token from cookies (Django uses it to prevent Cross-Site Request Forgery)
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  
    const csrfToken = getCookie("csrftoken"); // ✅ Extracted from browser cookies
    console.log("🔐 CSRF Token:", csrfToken); // 👀 Useful for debugging
  
    // 🎯 Get references to important DOM elements using their IDs
    const machineSelect = document.getElementById("machine");   // Dropdown menu to choose a machine
    const form = document.getElementById("fault-form");         // The form used to submit a fault report
    const result = document.getElementById("result");           // Paragraph where success or error messages will be displayed
  
    // 🔄 Fetch the list of machines from the backend API
    fetch("/api/machines/")
      .then(res => res.json()) // Parse the response from the server as JSON
      .then(data => {
        data.forEach(machine => {
          const option = document.createElement("option"); // Create a new <option> element
          option.value = machine.machine_id;
          option.textContent = `${machine.name} (${machine.status})`;
          machineSelect.appendChild(option);
        });
      });
  
    // 📤 Listen for form submission and handle it using JavaScript
    form.addEventListener("submit", async (e) => {
      e.preventDefault(); // Prevents page reload
      console.log("📤 Submitting fault report...");
  
      // 🧱 Prepare the data to be sent to the backend
      const payload = {
        machine: machineSelect.value,
        note: document.getElementById("note").value,
        created_by: document.getElementById("created_by").value // ✅ Manually entered username
      };
      console.log("📦 Payload:", payload);
  
      try {
        // 📡 Send the data to the backend API using a POST request
        const response = await fetch("/api/fault-cases/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken // ✅ Send CSRF token in header
          },
          credentials: "same-origin", // ✅ Include cookies with request (for session authentication)
          body: JSON.stringify(payload)
        });
  
        // ✅ Handle the server's response
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