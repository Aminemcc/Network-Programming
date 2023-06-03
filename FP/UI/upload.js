document.addEventListener("DOMContentLoaded", function () {
    const dropArea = document.querySelector(".drop_box");
    const button = dropArea.querySelector("button");
    const input = dropArea.querySelector("input");
  
    button.onclick = () => {
      input.click();
    };
  
    input.addEventListener("change", function (e) {
      const fileName = e.target.files[0].name;
      const filedata = `
        <form action="" method="post">
          <div class="form">
            <h4>${fileName}</h4>
            <input type="email" placeholder="Enter email upload file">
            <button class="btn">Upload</button>
          </div>
        </form>`;
      dropArea.innerHTML = filedata;
    });
  });
  