// Attach an event listener to the login form to intercept the submission
document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent the default form submission behavior (which would reload the page)
  
    // Get the input values and trim whitespace
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
  
    // Basic frontend validation to ensure both fields are filled
    if (!username || !password) {
      alert("All fields are required!");
      return; // Stop the script if validation fails
    }
  
    try {
      // Attempt to log the user in using Django's built-in login view at /accounts/login/
      const response = await fetch("/accounts/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded", // Required format for Django’s default login
        },
        body: new URLSearchParams({
          username: username,
          password: password,
        }), // Format the body like a traditional HTML form
        credentials: "include" // Ensure cookies (like sessionid) are included in the request
      });
  
      // If the login is successful, redirect the user to the dashboard
      if (response.ok) {
        window.location.href = "/dashboard/";
      } else {
        // If the login failed (e.g., wrong credentials), notify the user
        alert("Login failed. Please check your credentials.");
      }
    } catch (error) {
      // Handle unexpected errors (e.g., network issues)
      console.error("Login error:", error);
      alert("Something went wrong. Please try again later.");
    }
  });