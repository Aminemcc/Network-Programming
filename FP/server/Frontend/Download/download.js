document.addEventListener("DOMContentLoaded", function() {
  const modal = document.getElementById("myModal");
  const closeBtn = document.querySelector(".close");
  const responseMessageElement = document.getElementById("responseMessage");

  function showModal(responseMessage) {
    responseMessageElement.textContent = responseMessage;
    modal.style.display = "block";
  }

  function closeModal() {
    modal.style.display = "none";
  }

  closeBtn.addEventListener("click", closeModal);

  window.addEventListener("click", function (event) {
    if (event.target == modal) {
      closeModal();
    }
  });

  function submitForm(event) {
    event.preventDefault();
  
    const form = document.getElementById("stripe-login");
    const formData = new FormData(form);
  
    fetch("http://localhost:8000/download", {
      method: "POST",
      body: formData,
    })
      .then(function (response) {
        if (response.ok) {
          return response.blob();  // Retrieve the response as a Blob object
        } else {
          throw new Error("Error occurred during form submission.");
        }
      })
      .then(function (blob) {
        const url = URL.createObjectURL(blob);  // Create a URL for the Blob object
        downloadFile(url, formData);  // Pass formData as an argument to downloadFile function
      })
      .catch(function (error) {
        console.error(error);
        showModal("An error occurred during form submission.");
      });
  }

  function downloadFile(url, formData) {
    const link = document.createElement("a");
    link.href = url;
    const filename = formData.get("nama_file");
    link.download = filename || "unknown";
  
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  

  const form = document.getElementById("stripe-login");
  form.addEventListener("submit", submitForm);
});
