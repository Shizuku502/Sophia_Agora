// static/js/teacher_schedule.js

document.addEventListener("DOMContentLoaded", () => {
  const PERIOD_TIME_MAP = {
    1: ["08:10", "09:00"],
    2: ["09:10", "10:00"],
    3: ["10:10", "11:00"],
    4: ["11:10", "12:00"],
    5: ["12:10", "13:00"],
    6: ["13:10", "14:00"],
    7: ["14:10", "15:00"],
    8: ["15:10", "16:00"],
  };

  const scheduleBody = document.getElementById("schedule-body");
  const addModal = new bootstrap.Modal(document.getElementById("addScheduleModal"));
  const editModal = new bootstrap.Modal(document.getElementById("editScheduleModal"));
  let currentEditId = null;

  function loadSchedules() {
    fetch("/api/teacher/schedules")
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then(data => renderTable(data))
      .catch(err => {
        alert("載入課表失敗");
        console.error(err);
      });
  }

  function renderTable(schedules) {
    scheduleBody.innerHTML = "";
    // 建立 8x7 空表格
    const tableData = Array.from({ length: 8 }, () => Array(7).fill(null));

    schedules.forEach(s => {
      // s.weekday 0=星期一，p 節次
      const period = Object.entries(PERIOD_TIME_MAP).find(
        ([key, val]) => val[0] === s.start_time && val[1] === s.end_time
      )?.[0];
      if (period !== undefined) {
        tableData[period - 1][s.weekday] = s;
      }
    });

    for (let p = 1; p <= 8; p++) {
      const tr = document.createElement("tr");

      // 節次欄
      const tdPeriod = document.createElement("td");
      tdPeriod.innerHTML = `${p}<br><small>${PERIOD_TIME_MAP[p][0]}~${PERIOD_TIME_MAP[p][1]}</small>`;
      tr.appendChild(tdPeriod);

      for (let wd = 0; wd < 7; wd++) {
        const td = document.createElement("td");
        const entry = tableData[p - 1][wd];
        if (entry) {
          td.innerHTML = `${entry.course_name}<br><small>${entry.location}</small>`;
          td.classList.add("clickable");
          td.style.cursor = "pointer";  // 確保有 pointer 樣式
          td.addEventListener("click", () => openEditModal(entry.id));
        } else {
          td.innerHTML = ""; // 空白格子
        }
        tr.appendChild(td);
      }
      scheduleBody.appendChild(tr);
    }
  }

  document.getElementById("add-schedule-form").addEventListener("submit", e => {
    e.preventDefault();
    const weekday = parseInt(document.getElementById("weekday-select").value);
    const course_name = document.getElementById("course-name-input").value.trim();
    const location = document.getElementById("location-input").value.trim();
    const periods = [...document.querySelectorAll("input[name='periods']:checked")].map(el => parseInt(el.value));

    if (isNaN(weekday) || !course_name || !location || periods.length === 0) {
      alert("請完整填寫所有欄位");
      return;
    }

    fetch("/api/teacher/schedules", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ weekday, periods, course_name, location }),
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) alert("新增失敗：" + data.error);
        else {
          alert("新增成功！");
          document.getElementById("add-schedule-form").reset();
          addModal.hide();
          loadSchedules();
        }
      })
      .catch(err => {
        alert("新增發生錯誤");
        console.error(err);
      });
  });

  function openEditModal(id) {
    fetch(`/api/teacher/schedules/${id}`)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then(data => {
        currentEditId = id;
        document.getElementById("edit-weekday-select").value = data.weekday;
        document.getElementById("edit-period-select").value = data.period;
        document.getElementById("edit-course-name-input").value = data.course_name;
        document.getElementById("edit-location-input").value = data.location;
        editModal.show();
      })
      .catch(err => {
        alert("載入失敗");
        console.error(err);
      });
  }

  document.getElementById("edit-schedule-form").addEventListener("submit", e => {
    e.preventDefault();
    const weekday = parseInt(document.getElementById("edit-weekday-select").value);
    const period = parseInt(document.getElementById("edit-period-select").value);
    const course_name = document.getElementById("edit-course-name-input").value.trim();
    const location = document.getElementById("edit-location-input").value.trim();

    if (isNaN(weekday) || isNaN(period) || !course_name || !location) {
      alert("請完整填寫所有欄位");
      return;
    }

    fetch(`/api/teacher/schedules/${currentEditId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ weekday, period, course_name, location }),
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) alert("更新失敗：" + data.error);
        else {
          alert("更新成功！");
          editModal.hide();
          loadSchedules();
        }
      })
      .catch(err => {
        alert("更新發生錯誤");
        console.error(err);
      });
  });

  document.getElementById("delete-schedule-btn").addEventListener("click", () => {
    if (!confirm("確定要刪除這堂課？")) return;
    fetch(`/api/teacher/schedules/${currentEditId}`, { method: "DELETE" })
      .then(res => res.json())
      .then(data => {
        if (data.error) alert("刪除失敗：" + data.error);
        else {
          alert("刪除成功");
          editModal.hide();
          loadSchedules();
        }
      })
      .catch(err => {
        alert("刪除發生錯誤");
        console.error(err);
      });
  });

  loadSchedules();
});
