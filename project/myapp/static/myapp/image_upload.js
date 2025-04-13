// Wait until the entire HTML document is fully loaded before running the script
document.addEventListener("DOMContentLoaded", () => {

    // Helper function to get the CSRF token from browser cookies
    // Django requires this token to protect against CSRF attacks on POST requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");  // Split all cookies
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();  // Remove whitespace
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    // Decode and return the cookie value if it matches
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;  // Return the CSRF token
    }

    const csrfToken = getCookie("csrftoken");  // Store the CSRF token
    console.log("CSRF Token:", csrfToken);     // Log for debugging

    // Reference to the upload form and result paragraph in the HTML
    const form = document.getElementById("image-upload-form");
    const result = document.getElementById("upload-result");

    // Event listener for form submission
    form.addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevent default form submission (page reload)

        // Get input values: fault note ID and image file
        const faultNoteId = document.getElementById("fault_note_id").value;
        const imageFile = document.getElementById("image").files[0];

        // Log data to make sure it's being collected correctly
        console.log("Uploading for FaultNote ID:", faultNoteId);
        console.log("Image file:", imageFile);

        // Create a FormData object to send binary image + text
        const formData = new FormData();
        formData.append("fault_note", faultNoteId);  // ID of the FaultNote
        formData.append("image", imageFile);         // Image file object

        try {
            // Send a POST request to the API endpoint
            const response = await fetch("/api/fault-note-images/", {
                method: "POST",          // Use POST to upload the file
                headers: {
                    "X-CSRFToken": csrfToken  // Add CSRF token to headers
                },
                credentials: "same-origin",   // Include cookies for authentication
                body: formData                // Send FormData (not JSON)
            });

            if (response.ok) {
                // Success — inform the user
                result.textContent = "✅ Image uploaded successfully!";
                result.style.color = "green";
                form.reset();  // Clear the form
            } else {
                // Error — show details from the server
                const err = await response.json();
                result.textContent = "❌ Error: " + JSON.stringify(err);
                result.style.color = "red";
            }
        } catch (error) {
            // Handle connection or unexpected errors
            result.textContent = "❌ Upload failed: " + error;
            result.style.color = "red";
        }
    });
});