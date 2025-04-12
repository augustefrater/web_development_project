document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
  
    if (!username || !password) {
      alert("All fields are required!");
    } else {
      alert("Login successful! (Simulated)");
      window.location.href = "dashboard.html";
    }
  });
  