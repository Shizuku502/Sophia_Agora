// static/js/add_appointment.js

document.addEventListener("DOMContentLoaded", async () => {
  const slotContainer = document.getElementById("available-slots");
  const modal = document.getElementById("appointment-modal");
  const closeBtn = modal.querySelector(".close-button");
  const reasonInput = document.getElementById("appointment-reason");
  const submitBtn = document.getElementById("submit-appointment");
  const selectedSlotInfo = document.getElementById("selected-slot-info");

  let selectedSlot = null; // { slot_id, date, start_time, end_time }

  // 取得該教師的可預約時間
  try {
    const res = await axios.get(`/api/appointment/teacher/${teacherId}/available_slots`);
    const slots = res.data.slots || [];

    if (slots.length === 0) {
      slotContainer.innerHTML = "<p>目前沒有開放預約的時間。</p>";
    } else {
      slotContainer.innerHTML = "";
      slots.forEach(slot => {
        const btn = document.createElement("button");
        btn.classList.add("slot-button");
        btn.textContent = `${slot.date} ${slot.start_time} - ${slot.end_time}`;
        btn.addEventListener("click", () => {
          selectedSlot = slot;
          selectedSlotInfo.textContent = btn.textContent;
          reasonInput.value = "";
          modal.style.display = "block";
        });
        slotContainer.appendChild(btn);
      });
    }
  } catch (err) {
    slotContainer.innerHTML = "<p>無法載入可預約時間。</p>";
  }

  // Modal 關閉
  closeBtn.onclick = () => (modal.style.display = "none");
  window.onclick = e => {
    if (e.target === modal) modal.style.display = "none";
  };

  // 預約送出
  submitBtn.addEventListener("click", async () => {
    const reason = reasonInput.value.trim();
    if (!reason) {
      alert("請輸入預約動機");
      return;
    }
    if (!selectedSlot) {
      alert("請先選擇預約時段");
      return;
    }

    try {
      await axios.post("/api/appointment/add", {
        slot_id: selectedSlot.slot_id,
        date: selectedSlot.date,
        reason: reason
      });

      alert("預約已送出！");
      modal.style.display = "none";
    } catch (err) {
      alert("預約失敗，請稍後再試。");
    }
  });
});
