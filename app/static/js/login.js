// app/static/js/login.js
document.addEventListener("DOMContentLoaded", function () {
  const pwdInput = document.getElementById("password");
  const toggleBtn = document.getElementById("toggleBtn");

  toggleBtn.addEventListener("click", function () {
    if (pwdInput.type === "password") {
      pwdInput.type = "text";
      toggleBtn.textContent = "隱藏";
    } else {
      pwdInput.type = "password";
      toggleBtn.textContent = "顯示";
    }
  });
});
