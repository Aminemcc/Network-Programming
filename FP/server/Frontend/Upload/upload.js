document.addEventListener("DOMContentLoaded", function () {
  const dropArea = document.querySelector(".drop_box");
  const button = dropArea.querySelector("button");
  const input = dropArea.querySelector("input");

  button.onclick = () => {
    input.click();
  };

  input.addEventListener("change", function (e) {
    const file = e.target.files[0];

    console.log("Uploading file:", file.name);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload/' + file.name, true);

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          // File uploaded successfully
          console.log('File uploaded successfully.');
        } else {
          // Error occurred while uploading the file
          console.error('Error occurred while uploading the file.');
        }
      }
    };

    xhr.setRequestHeader('Content-Type', 'application/octet-stream');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest'); // Add this line to set the X-Requested-With header

    xhr.onloadstart = function () {
      console.log('Request started:', xhr.getAllResponseHeaders());
    };

    xhr.onloadend = function () {
      console.log('Request completed:', xhr.getAllResponseHeaders());
    };

    xhr.send(file);
  });
});
