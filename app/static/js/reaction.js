// static/js/reaction.js
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
    });
  });
});

function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? match[2] : null;
}