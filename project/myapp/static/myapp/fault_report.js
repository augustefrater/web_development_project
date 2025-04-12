// Wait for the full HTML document to be loaded before running the script
document.addEventListener("DOMContentLoaded", () => {

    // Get references to DOM elements using their IDs
    const machineSelect = document.getElementById("machine");   // The <select> dropdown for machine options
    const form = document.getElementById("fault-form");         // The form element to handle submissions
    const result = document.getElementById("result");           // Paragraph where success/error messages will be displayed
  
    // Fetch the list of machines from the API to populate the dropdown
    fetch("/api/machines/")
      .then(res => res.json()) // Parse the JSON response
      .then(data => {
        // For each machine received from the API, create an <option> element
        data.forEach(machine => {
          const option = document.createElement("option");
          option.value = machine.machine_id; // Set the option's value to the machine ID
          option.textContent = `${machine.name} (${machine.status})`; // Display machine name and status
          machineSelect.appendChild(option); // Add the option to the dropdown
        });
      });
  
    // Listen for the form submission event
    form.addEventListener("submit", async (e) => {
      e.preventDefault(); // Prevent the default form submission (which would reload the page)
  
      // Build the payload to be sent to the backend
      const payload = {
        machine: machineSelect.value,                           // Selected machine ID
        note: document.getElementById("note").value             // Text entered in the note field
      };
  
      try {
        // Send a POST request to the fault-cases API endpoint
        const response = await fetch("/api/fault-cases/", {
          method: "POST",                                       // HTTP method
          headers: {
            "Content-Type": "application/json"                 // Inform the server we’re sending JSON
          },
          body: JSON.stringify(payload)                        // Convert the payload to a JSON string
        });
  
        if (response.ok) {
          // If the request was successful, show a confirmation and reset the form
          result.textContent = "✅ Fault report submitted!";
          form.reset();
        } else {
          // If the server returns an error, parse and show it
          const err = await response.json();
          result.textContent = "❌ Error: " + JSON.stringify(err);
        }
      } catch (error) {
        // If the request fails (e.g., network error), show the error
        result.textContent = "❌ Request failed: " + error;
      }
    });
  });