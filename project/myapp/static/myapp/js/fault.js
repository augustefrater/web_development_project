document.getElementById("faultForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const machineID = document.getElementById("machineID").value;
    const description = document.getElementById("description").value;
  
    if (!machineID || !description) {
      alert("Please fill out all required fields.");
    } else {
      alert("Fault submitted successfully!");
      this.reset();
    }
  });
  