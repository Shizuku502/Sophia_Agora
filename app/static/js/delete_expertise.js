// static/js/delete_expertise.js

document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".btn-delete-expertise");

    deleteButtons.forEach((button) => {
        // 若已綁定事件，則不再重複綁定
        if (button.dataset.bound === "true") return;
        button.dataset.bound = "true"; // 標記已綁定

        let isDeleting = false; // 每顆按鈕獨立旗標

        button.addEventListener("click", function () {
            if (isDeleting) return;
            isDeleting = true;

            const expertiseId = this.dataset.expertiseId;
            const url = `/teacher/expertises/delete/${expertiseId}`;
            const li = this.closest("li");

            if (!expertiseId || !li) {
                isDeleting = false;
                return;
            }

            if (confirm("確定要刪除此專長嗎？")) {
                csrfPost(url, { expertise_id: expertiseId })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            li.classList.add("fade-out");
                            setTimeout(() => li.remove(), 300);
                            dispatchToast("success", "已成功刪除研究專長");
                        } else {
                            dispatchToast("error", data.message || "刪除失敗");
                        }
                    })
                    .catch(() => {
                        dispatchToast("error", "刪除請求發生錯誤");
                    })
                    .finally(() => {
                        isDeleting = false;
                    });
            } else {
                isDeleting = false; // 使用者取消
            }
        });
    });
});
