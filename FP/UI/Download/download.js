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
            return response.text();
          } else {
            throw new Error("Error occurred during form submission.");
          }
        })
        .then(function (data) {
          showModal(data);
        })
        .catch(function (error) {
          console.error(error);
          showModal("An error occurred during form submission.");
        });
    }
  
    const form = document.getElementById("stripe-login");
    form.addEventListener("submit", submitForm);
  });
  