// static/js/edit_experience.js

document.addEventListener("DOMContentLoaded", () => {
    const experienceList = document.getElementById("experience-list");
    const editForm = document.getElementById("edit-experience-form");
    const form = document.getElementById("experience-edit-form");

    if (!form || form.dataset.bound === "true") return; // 防止重複綁定

    const categoryInput = document.getElementById("edit-category");
    const descriptionInput = document.getElementById("edit-description");
    const expIdInput = document.getElementById("edit-exp-id");
    const cancelBtn = document.getElementById("cancel-edit");

    form.dataset.bound = "true"; // 註記已綁定

    experienceList.addEventListener("click", (e) => {
        if (e.target.classList.contains("btn-edit-experience")) {
            const li = e.target.closest("li");
            const expId = li.getAttribute("data-id");
            const category = li.querySelector(".experience-badge").textContent.trim();
            const description = li.querySelector(".experience-description").textContent.trim();

            expIdInput.value = expId;
            categoryInput.value = category;
            descriptionInput.value = description;

            editForm.style.display = "block";
            editForm.scrollIntoView({ behavior: "smooth" });
        }
    });

    cancelBtn.addEventListener("click", () => {
        editForm.style.display = "none";
        form.reset();
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // 很重要，防止瀏覽器預設提交！

        const expId = expIdInput.value;
        const category = categoryInput.value.trim();
        const description = descriptionInput.value.trim();

        if (!category || !description) {
            alert("所有欄位皆為必填！");
            return;
        }

        try {
            const response = await csrfPost(`/teacher/experiences/edit/${expId}`, {
                category,
                description
            });

            const result = await response.json();

            if (response.ok && result.success) {
                const li = document.querySelector(`li[data-id="${expId}"]`);
                li.querySelector(".experience-badge").textContent = category;
                li.querySelector(".experience-description").textContent = description;

                alert("更新成功！");
                form.reset();
                editForm.style.display = "none";
            } else {
                alert(result.error || "更新失敗！");
            }
        } catch (err) {
            console.error("AJAX 錯誤", err);
            alert("與伺服器連線失敗！");
        }
    });
});

