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

    document.addEventListener('DOMContentLoaded', function() {
      // File upload preview
      const imageUpload = document.getElementById('imageUpload');
      const filePreview = document.getElementById('filePreview');
      const filePreviewName = document.querySelector('.file-preview-name');
      const filePreviewSize = document.querySelector('.file-preview-size');
      const removeFileBtn = document.getElementById('removeFile');
      
      imageUpload.addEventListener('change', function(e) {
        if (this.files.length > 0) {
          const file = this.files[0];
          filePreviewName.textContent = file.name;
          
          // Format file size
          let size = file.size;
          let sizeText = '';
          
          if (size < 1024) {
            sizeText = size + ' B';
          } else if (size < 1024 * 1024) {
            sizeText = (size / 1024).toFixed(1) + ' KB';
          } else {
            sizeText = (size / (1024 * 1024)).toFixed(1) + ' MB';
          }
          
          filePreviewSize.textContent = sizeText;
          filePreview.classList.add('active');
          
          // If it's an image, show preview
          if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
              document.querySelector('.file-preview-image').src = e.target.result;
            };
            reader.readAsDataURL(file);
          } else {
            // For non-image files, show generic icon
            document.querySelector('.file-preview-image').src = '/api/placeholder/60/60';
          }
        }
      });
      
      removeFileBtn.addEventListener('click', function() {
        imageUpload.value = '';
        filePreview.classList.remove('active');
      });
      
      // Form submission
      const faultForm = document.getElementById('faultForm');
      const successMessage = document.getElementById('successMessage');
      
      faultForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Simulate form submission
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        
        // Simulate network delay
        setTimeout(() => {
          successMessage.classList.add('active');
          submitBtn.textContent = 'Submit Fault Report';
          submitBtn.disabled = false;
          
          // Scroll to top to show success message
          window.scrollTo({
            top: 0,
            behavior: 'smooth'
          });
          
          // Reset form after submission
          faultForm.reset();
          filePreview.classList.remove('active');
        }, 1500);
      });
      
      // Cancel button
      const cancelBtn = document.getElementById('cancelBtn');
      cancelBtn.addEventListener('click', function() {
        // Just reset the form for this demo
        faultForm.reset();
        filePreview.classList.remove('active');
        successMessage.classList.remove('active');
      });
    });
  