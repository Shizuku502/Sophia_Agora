// app/static/js/student_appointment.js

document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.querySelector('#appointment-table tbody');
    const messageDiv = document.getElementById('message');

    // 讀取學生所有預約
    function loadAppointments() {
        fetch('/api/appointment/student/list')
            .then(res => res.json())
            .then(data => {
                tableBody.innerHTML = '';
                if (!data.appointments || data.appointments.length === 0) {
                    tableBody.innerHTML = `<tr><td colspan="6">尚無預約紀錄</td></tr>`;
                    return;
                }

                data.appointments.forEach(app => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${app.teacher_name}</td>
                        <td>${app.date}</td>
                        <td>${app.start_time} - ${app.end_time}</td>
                        <td>${app.status}</td>
                        <td>${app.note || ''}</td>
                        <td>
                            ${
                              (app.status === 'pending' || app.status === 'accepted') 
                              ? `<button data-id="${app.id}" class="cancel-btn">取消預約</button>` 
                              : ''
                            }
                        </td>
                    `;
                    tableBody.appendChild(tr);
                });

                // 綁定取消按鈕事件
                document.querySelectorAll('.cancel-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        const id = btn.getAttribute('data-id');
                        if (confirm('確定要取消這個預約嗎？')) {
                            cancelAppointment(id);
                        }
                    });
                });
            })
            .catch(err => {
                messageDiv.textContent = '載入預約資料失敗';
                console.error(err);
            });
    }

    // 取消預約
    function cancelAppointment(id) {
        fetch(`/api/appointment/cancel/${id}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                messageDiv.textContent = `錯誤：${data.error}`;
            } else {
                messageDiv.textContent = data.message || '已取消預約';
                loadAppointments();
            }
        })
        .catch(err => {
            messageDiv.textContent = '取消預約失敗';
            console.error(err);
        });
    }

    loadAppointments();
});
