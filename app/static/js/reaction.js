document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".reaction-btn").forEach(button => {
    button.addEventListener("click", async (e) => {
      const btn = e.currentTarget;
      const type = btn.dataset.type;
      const parent = btn.closest(".reaction-buttons");
      const postId = parent.dataset.postId || null;
      const commentId = parent.dataset.commentId || null;

      const response = await fetch("/reactions/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrf_token")
        },
        body: JSON.stringify({
          post_id: postId,
          comment_id: commentId,
          type: type
        })
      });

      const result = await response.json();

      if (result.status) {
        // 刷新頁面數據或動態更新
        window.location.reload();
      }
    });
  });
});

function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? match[2] : null;
}