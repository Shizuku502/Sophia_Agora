// app/static/js/available_slots.js

document.addEventListener("DOMContentLoaded", () => {
  const weekdaySelect = document.getElementById("weekday");
  const slotList = document.getElementById("slotList");

  // 讀取目前的可預約時段
  function loadSlots() {
    fetch("/api/teacher/available_slots")
      .then(res => res.json())
      .then(data => {
        slotList.innerHTML = "";
        data.forEach(slot => {
          const item = document.createElement("li");
          item.className = "list-group-item d-flex justify-content-between align-items-center";

          item.innerHTML = `
            星期${parseInt(slot.weekday) + 1}：${slot.start_time} - ${slot.end_time}
            <button class="btn btn-danger btn-sm" data-id="${slot.id}">刪除</button>
          `;

          // 加入刪除事件
          const deleteBtn = item.querySelector("button");
          deleteBtn.addEventListener("click", () => {
            deleteSlot(slot.id);
          });

          slotList.appendChild(item);
        });
      });
  }

  // 新增可預約時段
  document.getElementById("slotForm").addEventListener("submit", e => {
    e.preventDefault();
    const weekday = parseInt(weekdaySelect.value);
    const periods = Array.from(document.querySelectorAll("input[type='checkbox']:checked"))
                         .map(cb => parseInt(cb.value));

    if (periods.length === 0) {
      alert("請至少選擇一個節次！");
      return;
    }

    fetch("/api/teacher/available_slots", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ weekday, periods })
    })
    .then(res => res.json())
    .then(data => {
      alert(data.message);
      loadSlots();
    });
  });

  // 刪除單一時段
  function deleteSlot(slotId) {
    if (!confirm("確定要刪除此時段嗎？")) return;

    fetch(`/api/teacher/available_slots/${slotId}`, {
      method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
      alert(data.message || "刪除成功");
      loadSlots();
    })
    .catch(() => {
      alert("刪除失敗，請稍後再試");
    });
  }

  loadSlots();
});

