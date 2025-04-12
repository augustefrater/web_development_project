
  function validateSignup() {
    const pw = document.getElementById("password").value;
    const cpw = document.getElementById("confirm").value;
    const terms = document.getElementById("terms").checked;
  
    if (pw !== cpw) {
      alert("Passwords do not match!");
      return false;
    }
  
    if (!terms) {
      alert("You must accept the terms and conditions.");
      return false;
    }
  
    alert("Signup successful! ");
    window.location.href = "index.html"; // Instant redirect
  
    return false; // Prevent default form submission
  }
  