// static/js/delete_paper.js

document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".btn-delete-paper");

    deleteButtons.forEach(function (button) {
        // 如果已經綁定過就不要再綁一次
        if (button.dataset.bound === "true") return;

        button.dataset.bound = "true";

        button.addEventListener("click", function (e) {
            e.preventDefault(); // 阻止表單或其他事件冒泡
            const paperId = this.getAttribute("data-paper-id");

            if (!confirm("你確定要刪除此篇論文嗎？")) {
                return;
            }

            fetch(`/teacher/papers/delete/${paperId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        alert("刪除成功");
                        const li = button.closest("li");
                        if (li) li.remove();
                    } else {
                        alert("刪除失敗：" + data.message);
                    }
                })
                .catch((error) => {
                    alert("發生錯誤，請稍後再試");
                    console.error("刪除錯誤：", error);
                });
        });
    });
});
