// app/static/js/teacher_appointment.js

document.addEventListener("DOMContentLoaded", () => {
    fetchAppointments();

    document.getElementById("cancelRejectBtn").addEventListener("click", () => {
        document.getElementById("rejectModal").style.display = "none";
    });

    document.getElementById("confirmRejectBtn").addEventListener("click", () => {
        const reason = document.getElementById("rejectionReason").value.trim();
        const appointmentId = document.getElementById("rejectModal").dataset.appointmentId;
        if (!reason) {
            alert("請輸入拒絕原因！");
            return;
        }
        handleReject(appointmentId, reason);
    });

    document.getElementById("filter-pending").addEventListener("change", fetchAppointments);
});

function fetchAppointments() {
    fetch("/api/appointment/teacher/list")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("appointment-list");
            list.innerHTML = "";

            const showPendingOnly = document.getElementById("filter-pending").checked;
            const filtered = showPendingOnly
                ? data.appointments.filter(app => app.status === "pending")
                : data.appointments;

            if (filtered.length === 0) {
                list.innerHTML = "<p>目前沒有符合條件的預約。</p>";
                return;
            }

            filtered.forEach(app => {
                const div = document.createElement("div");
                div.className = "appointment-item";
                div.innerHTML = `
                    <div class="appointment-header">
                        學生：${app.student_name}
                    </div>
                    <div class="appointment-body">
                        <p><strong>時間:</strong> ${app.date} ${app.start_time} - ${app.end_time}</p>
                        <p><strong>狀態:</strong> ${statusLabel(app.status)}</p>
                        ${app.note ? `<p><strong>學生理由:</strong> ${app.note}</p>` : ""}
                        ${app.status === "rejected" && app.rejection_reason ? `<p><strong>拒絕原因:</strong> ${app.rejection_reason}</p>` : ""}
                        ${app.status === "pending" ? `
                            <div class="appointment-buttons">
                                <button onclick="handleAccept(${app.id})">接受</button>
                                <button onclick="openRejectModal(${app.id})">拒絕</button>
                            </div>
                        ` : ""}
                    </div>
                `;
                list.appendChild(div);
            });
        });
}

function statusLabel(status) {
    switch (status) {
        case "pending": return "待處理";
        case "accepted": return "已接受";
        case "rejected": return "已拒絕";
        default: return status;
    }
}

function handleAccept(id) {
    fetch(`/api/appointment/teacher/respond/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "accept" })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || "預約已接受");
        fetchAppointments();
    })
    .catch(() => alert("處理失敗，請稍後再試"));
}

function openRejectModal(id) {
    document.getElementById("rejectionReason").value = "";
    const modal = document.getElementById("rejectModal");
    modal.style.display = "block";
    modal.dataset.appointmentId = id;
}

function handleReject(id, reason) {
    fetch(`/api/appointment/teacher/respond/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "reject", reason })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message || "預約已拒絕");
        document.getElementById("rejectModal").style.display = "none";
        fetchAppointments();
    })
    .catch(() => alert("處理失敗，請稍後再試"));
}
