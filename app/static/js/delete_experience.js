// static/js/delete_experience.js

document.addEventListener("DOMContentLoaded", function () {
    document.body.addEventListener("click", function (e) {
        const button = e.target.closest(".btn-delete-experience");
        if (!button) return;

        // 避免重複點擊
        if (button.dataset.deleting === "true") return;
        button.dataset.deleting = "true";

        const experienceId = button.dataset.experienceId;
        const li = button.closest("li");

        if (!experienceId || !li) {
            button.dataset.deleting = "false";
            return;
        }

        if (!confirm("確定要刪除此經歷嗎？")) {
            button.dataset.deleting = "false";
            return;
        }

        const url = `/teacher/experiences/delete/${experienceId}`;

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest"
            },
            body: JSON.stringify({ experience_id: experienceId })
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    li.classList.add("fade-out");
                    setTimeout(() => li.remove(), 300);
                    dispatchToast("success", "已成功刪除經歷");
                } else {
                    dispatchToast("error", data.message || "刪除失敗");
                }
            })
            .catch(() => {
                dispatchToast("error", "刪除請求發生錯誤");
            })
            .finally(() => {
                button.dataset.deleting = "false";
            });
    });
});
