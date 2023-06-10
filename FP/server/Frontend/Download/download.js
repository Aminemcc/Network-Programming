document.addEventListener("DOMContentLoaded", function() {

  const form = document.getElementById("stripe-login");
  const submitButton = form.querySelector("input[type='submit']");

  submitButton.addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default form submission

    const fileNameInput = document.getElementById("nama_file");
    const fileName = fileNameInput.value;

    window.location.href = `http://localhost:8000/download/${fileName}`;
  });

});
