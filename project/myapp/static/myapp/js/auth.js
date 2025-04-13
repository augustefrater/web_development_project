document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  form?.addEventListener("submit", (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value;

    const storedUser = JSON.parse(localStorage.getItem("user"));

    if (
      storedUser?.username === username &&
      storedUser?.password === password &&
      storedUser?.role === role
    ) {
      localStorage.setItem(
        "loggedInUser",
        JSON.stringify({ username, role })
      );
      window.location.href = "profile.html";
    } else {
      alert("Invalid credentials or role mismatch.");
    }
  });
});
