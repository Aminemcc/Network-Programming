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
        downloadFile(url);  // Call the downloadFile function to initiate the file download
      })
      .catch(function (error) {
        console.error(error);
        showModal("An error occurred during form submission.");
      });
  }

  function downloadFile(url) {
    const link = document.createElement("a");
    link.href = url;
    link.download = "729.txt";  // Provide a default file name for the downloaded file
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  
  

  const form = document.getElementById("stripe-login");
  form.addEventListener("submit", submitForm);
});
