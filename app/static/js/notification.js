// static/js/notification.js

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".reaction-btn").forEach(button => {
    button.addEventListener("click", async (e) => {
      const btn = e.currentTarget;
      const type = btn.dataset.type;
      const parent = btn.closest(".reaction-buttons");
      const postId = parent.dataset.postId || null;
      const commentId = parent.dataset.commentId || null;

      const likeBtn = parent.querySelector(".reaction-btn.like");
      const dislikeBtn = parent.querySelector(".reaction-btn.dislike");
      const likeCountSpan = likeBtn.querySelector(".like-count");
      const dislikeCountSpan = dislikeBtn.querySelector(".dislike-count");

      // 禁用按鈕，顯示 loading 樣式
      btn.disabled = true;
      btn.classList.add("loading");

      try {
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

        if (["added", "updated", "removed"].includes(result.status)) {
          likeCountSpan.textContent = result.like_count;
          dislikeCountSpan.textContent = result.dislike_count;

          likeBtn.classList.remove("active-like");
          dislikeBtn.classList.remove("active-dislike");

          if (result.status === "added" || result.status === "updated") {
            if (type === "like") likeBtn.classList.add("active-like");
            else dislikeBtn.classList.add("active-dislike");
          }
        }
      } catch (error) {
        console.error("Reaction error:", error);
      } finally {
        btn.disabled = false;
        btn.classList.remove("loading");
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // ⏰ 鈴鐺點擊時，載入通知
  const notifBell = document.getElementById("notif-bell");
  const notifMenu = document.getElementById("notif-menu");
  const notifItems = document.getElementById("notif-items");

  notifBell.addEventListener("click", async () => {
    // 切換下拉選單顯示
    notifMenu.classList.toggle("show");

    // 如果已經載入過就不重複 fetch（你可以加一個 flag）
    if (!notifItems.dataset.loaded) {
      try {
        const response = await fetch("/notification/api/unread");
        const data = await response.json();

        notifItems.innerHTML = "";

        if (data.notifications.length === 0) {
          notifItems.innerHTML = "<p class='text-muted text-center m-2'>沒有新通知</p>";
        } else {
          data.notifications.forEach(n => {
            const item = document.createElement("div");
            item.classList.add("notif-item");
            item.innerHTML = `
              <a href="${n.link}" class="notif-link ${n.is_read ? '' : 'unread'}">
                ${n.content} <br><small>${n.created_at}</small>
              </a>
            `;
            notifItems.appendChild(item);
          });
        }

        notifItems.dataset.loaded = "true";  // 設為已載入
      } catch (error) {
        console.error("載入通知失敗:", error);
        notifItems.innerHTML = "<p class='text-danger text-center m-2'>載入失敗</p>";
      }
    }
  });
});

function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? match[2] : null;
}

