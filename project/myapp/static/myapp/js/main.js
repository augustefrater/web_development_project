window.addEventListener("DOMContentLoaded", () => {
    fetch("components/navbar.html").then(res => res.text()).then(data => {
      document.getElementById("navbar").innerHTML = data;
    });
  
    fetch("components/footer.html").then(res => res.text()).then(data => {
      document.getElementById("footer").innerHTML = data;
    });
  });

    // Maintain the same basic logic structure as requested
    document.addEventListener('DOMContentLoaded', function() {
      // This script would normally load navbar and footer components
      console.log('Page loaded successfully');
      
      // The original script would likely have included functions to load the navbar and footer
      // For this demo, we've built them directly into the HTML
    });
