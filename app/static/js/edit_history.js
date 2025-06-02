// static/js/edit_history.js

document.addEventListener("DOMContentLoaded", () => {
  // 處理留言編輯紀錄按鈕點擊事件
  document.querySelectorAll(".view-comment-history-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const commentId = btn.dataset.commentId;
      if (!commentId) return;

      try {
        const res = await fetch(`/comments/${commentId}/history`);
        const html = await res.text();
        const container = document.getElementById("dynamic-modal-container");
        if (container) {
          container.innerHTML = html;
          const modalEl = document.getElementById("commentHistoryModal");
          if (modalEl) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
          }
        }
      } catch (err) {
        console.error("載入留言歷史失敗：", err);
      }
    });
  });

  // 處理文章編輯紀錄按鈕點擊事件
  document.querySelectorAll(".view-post-history-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const postId = btn.dataset.postId;
      if (!postId) return;

      try {
        const res = await fetch(`/posts/${postId}/history`);
        const html = await res.text();
        const container = document.getElementById("dynamic-modal-container");
        if (container) {
          container.innerHTML = html;
          const modalEl = document.getElementById("postHistoryModal");
          if (modalEl) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
          }
        }
      } catch (err) {
        console.error("載入文章歷史失敗：", err);
      }
    });
  });
});
