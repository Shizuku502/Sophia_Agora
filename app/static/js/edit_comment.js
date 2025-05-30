// static/js/edit_comment.js

document.addEventListener("DOMContentLoaded", () => {
  const editButtons = document.querySelectorAll(".edit-comment-btn");
  const modal = new bootstrap.Modal(document.getElementById("editCommentModal"));
  const form = document.getElementById("editCommentForm");
  const textarea = document.getElementById("edit-comment-content");
  const commentIdInput = document.getElementById("edit-comment-id");

  editButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const commentId = btn.getAttribute("data-comment-id");
      try {
        const res = await fetch(`/comments/${commentId}/json`);
        if (!res.ok) throw new Error("無法取得留言資料，請稍後再試。");
        const data = await res.json();

        commentIdInput.value = data.id;
        textarea.value = data.content;
        modal.show();  // ✅ 確保 modal 顯示在資料載入後
      } catch (err) {
        alert(err.message);
      }
    });
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const commentId = commentIdInput.value;
    const content = textarea.value;

    try {
      const res = await fetch(`/comments/${commentId}/edit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ content }),
      });

      if (res.redirected) {
        window.location.href = res.url;
      } else if (res.ok) {
        // 更新畫面留言內容（無須整頁刷新）
        const commentEl = document.querySelector(`.edit-comment-btn[data-comment-id="${commentId}"]`).closest(".comment");
        commentEl.querySelector("p").innerHTML = `<strong>${commentEl.querySelector("strong").innerText}</strong>：${content}`;
        modal.hide();
      } else {
        throw new Error("更新留言失敗，請稍後再試。");
      }
    } catch (err) {
      alert(err.message);
    }
  });
});

