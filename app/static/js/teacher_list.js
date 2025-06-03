// static/js/teacher_list.js
document.addEventListener("DOMContentLoaded", () => {
  const copyElements = document.querySelectorAll(".copy-text");

  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    } else {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.style.position = "fixed";
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      try {
        document.execCommand("copy");
      } catch (err) {
        console.error("無法複製", err);
      }
      document.body.removeChild(textarea);
      return Promise.resolve();
    }
  }

  copyElements.forEach(el => {
    el.style.cursor = "pointer";
    el.title = "點擊複製";

    el.addEventListener("click", () => {
      const text = el.getAttribute("data-copy");

      copyToClipboard(text).then(() => {
        if (!el.hasAttribute("data-original")) {
          el.setAttribute("data-original", el.innerText);
        }
        el.classList.add("copied");
        el.innerText = text + "（已複製）";

        setTimeout(() => {
          el.innerText = el.getAttribute("data-original");
          el.classList.remove("copied");
        }, 1500);
      });
    });
  });
});
