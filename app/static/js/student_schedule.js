// app/static/js/student_schedule.js


document.addEventListener("DOMContentLoaded", () => {
    const scheduleTableBody = document.getElementById("schedule-body");
    const addScheduleForm = document.getElementById("add-schedule-form");
    const addScheduleModal = new bootstrap.Modal(document.getElementById('addScheduleModal'));

    const editScheduleModal = new bootstrap.Modal(document.getElementById("editScheduleModal"));
    const editScheduleForm = document.getElementById("edit-schedule-form");
    const editWeekdaySelect = document.getElementById("edit-weekday-select");
    const editPeriodSelect = document.getElementById("edit-period-select");
    const editCourseNameInput = document.getElementById("edit-course-name-input");
    const editLocationInput = document.getElementById("edit-location-input");
    const editDeleteBtn = document.getElementById("delete-schedule-btn");

    let currentEditId = null;

    const PERIOD_TIME_MAP = {
        1: ["08:10", "09:00"],
        2: ["09:10", "10:00"],
        3: ["10:10", "11:00"],
        4: ["11:10", "12:00"],
        5: ["12:10", "13:00"],
        6: ["13:10", "14:00"],
        7: ["14:10", "15:00"],
        8: ["15:10", "16:00"],
        9: ["16:10", "17:00"],
        10: ["17:10", "18:00"],
        11: ["18:10", "19:00"],
        12: ["19:10", "20:00"],
        13: ["20:10", "21:00"],
        14: ["21:10", "22:00"],
    };

    function loadSchedules() {
        fetch('/api/schedules')
            .then(response => response.json())
            .then(data => {
                renderScheduleTable(data);
            })
            .catch(err => {
                alert("無法載入課表資料！");
                console.error("載入課表失敗：", err);
            });
    }

    function renderScheduleTable(schedules) {
        scheduleTableBody.innerHTML = '';

        const maxPeriods = 14;
        const days = 7;
        const tableData = Array.from({ length: maxPeriods }, () => Array(days).fill(null));

        for (const s of schedules) {
            let period = null;
            for (const [key, val] of Object.entries(PERIOD_TIME_MAP)) {
                if (val[0] === s.start_time && val[1] === s.end_time) {
                    period = parseInt(key);
                    break;
                }
            }
            if (period !== null && s.weekday >= 0 && s.weekday < 7) {
                tableData[period - 1][s.weekday] = {
                    id: s.id,
                    course_name: s.course_name,
                    location: s.location
                };
            }
        }

        for (let p = 1; p <= maxPeriods; p++) {
            const tr = document.createElement("tr");

            const tdPeriod = document.createElement("td");
            tdPeriod.innerHTML = `${p}<br><small>${PERIOD_TIME_MAP[p][0]}~${PERIOD_TIME_MAP[p][1]}</small>`;
            tr.appendChild(tdPeriod);

            for (let wd = 0; wd < days; wd++) {
                const td = document.createElement("td");

                const entry = tableData[p - 1][wd];
                if (entry) {
                    td.innerHTML = `${entry.course_name}<br><small>${entry.location}</small>`;
                    td.classList.add("clickable");
                    td.dataset.scheduleId = entry.id;
                    td.addEventListener("click", () => openEditModal(entry.id));
                }

                tr.appendChild(td);
            }

            scheduleTableBody.appendChild(tr);
        }
    }

    addScheduleForm.addEventListener("submit", e => {
        e.preventDefault();

        const weekday = parseInt(document.getElementById("weekday-select").value);
        const course_name = document.getElementById("course-name-input").value.trim();
        const location = document.getElementById("location-input").value.trim();
        const checkedPeriods = [...document.querySelectorAll('input[name="periods"]:checked')].map(el => parseInt(el.value));

        if (isNaN(weekday)) {
            alert("請選擇星期");
            return;
        }
        if (checkedPeriods.length === 0) {
            alert("請至少選擇一個節次");
            return;
        }
        if (!course_name) {
            alert("請輸入課程名稱");
            return;
        }
        if (!location) {
            alert("請輸入地點");
            return;
        }

        fetch('/api/schedules', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                weekday,
                periods: checkedPeriods,
                course_name,
                location
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("新增失敗：" + data.error);
            } else {
                alert("新增成功！");
                addScheduleForm.reset();
                addScheduleModal.hide();
                loadSchedules();
            }
        })
        .catch(err => {
            alert("新增發生錯誤，請稍後再試");
            console.error(err);
        });
    });

    function openEditModal(id) {
        fetch(`/api/schedules/${id}`)
            .then(res => {
                if (!res.ok) {
                    return res.json().then(err => {
                        throw new Error(err.error || "未知錯誤");
                    });
                }
                return res.json();
            })
            .then(data => {
                currentEditId = id;
                editWeekdaySelect.value = data.weekday;
                editPeriodSelect.value = data.period;
                editCourseNameInput.value = data.course_name;
                editLocationInput.value = data.location;

                editScheduleModal.show();
            })
            .catch(err => {
                alert("載入課程資料失敗：" + err.message);
                console.error(err);
            });
    }

    editScheduleForm.addEventListener("submit", e => {
        e.preventDefault();

        const weekday = parseInt(editWeekdaySelect.value);
        const period = parseInt(editPeriodSelect.value);
        const course_name = editCourseNameInput.value.trim();
        const location = editLocationInput.value.trim();

        fetch(`/api/schedules/${currentEditId}`, {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                weekday,
                period,
                course_name,
                location
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("更新失敗：" + data.error);
            } else {
                alert("課程更新成功！");
                editScheduleModal.hide();
                loadSchedules();
            }
        })
        .catch(err => {
            alert("更新錯誤，請稍後再試");
            console.error(err);
        });
    });

    editDeleteBtn.addEventListener("click", () => {
        if (!confirm("確定要刪除這堂課嗎？")) return;

        fetch(`/api/schedules/${currentEditId}`, {
            method: "DELETE"
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("刪除失敗：" + data.error);
            } else {
                alert("課程已刪除");
                editScheduleModal.hide();
                loadSchedules();
            }
        })
        .catch(err => {
            alert("刪除錯誤，請稍後再試");
            console.error(err);
        });
    });

    loadSchedules();
});
