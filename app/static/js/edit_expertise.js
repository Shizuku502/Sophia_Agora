// app/static/js/edit_expertise.js

document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".expertise-item");

    items.forEach(item => {
        const editBtn = item.querySelector(".btn-edit-expertise");
        const saveBtn = item.querySelector(".btn-save-expertise");
        const cancelBtn = item.querySelector(".btn-cancel-expertise");
        const fieldText = item.querySelector(".field-text");
        const fieldInput = item.querySelector(".field-input");
        const expertiseId = item.closest("li").dataset.id;

        editBtn.addEventListener("click", () => {
            fieldText.style.display = "none";
            fieldInput.style.display = "inline-block";
            editBtn.style.display = "none";
            saveBtn.style.display = "inline-block";
            cancelBtn.style.display = "inline-block";
        });

        cancelBtn.addEventListener("click", () => {
            fieldInput.value = fieldText.textContent;
            fieldText.style.display = "inline-block";
            fieldInput.style.display = "none";
            editBtn.style.display = "inline-block";
            saveBtn.style.display = "none";
            cancelBtn.style.display = "none";
        });

        saveBtn.addEventListener("click", () => {
            const newValue = fieldInput.value.trim();
            if (!newValue) {
                alert("專長欄位不得為空");
                return;
            }

            csrfPost(`/teacher/expertises/edit/${expertiseId}`, { field: newValue })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        fieldText.textContent = newValue;
                        cancelBtn.click();
                    } else {
                        alert(data.message || "儲存失敗");
                    }
                })
                .catch(error => {
                    console.error("更新失敗", error);
                    alert("發生錯誤，請稍後再試。");
                });
        });
    });
});
