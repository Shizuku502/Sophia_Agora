// app/static/js/student_appointment.js

document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.querySelector('#appointment-table tbody');
    const messageDiv = document.getElementById('message');
    const filterPending = document.getElementById('filter-pending');

    const paginationDiv = document.getElementById('pagination');
    let currentPage = 1;

    // 載入學生預約
    function loadAppointments(page = 1) {
        fetch(`/api/appointment/student/list?page=${page}`)
            .then(res => res.json())
            .then(data => {
                tableBody.innerHTML = '';
                paginationDiv.innerHTML = '';
                currentPage = data.page;

                const filtered = data.appointments.filter(app => {
                    return !filterPending.checked || app.status === 'pending';
                });

                if (!filtered.length) {
                    tableBody.innerHTML = `<tr><td colspan="7">尚無預約紀錄</td></tr>`;
                    return;
                }

                filtered.forEach(app => {
                    const tr = document.createElement('tr');

                    let statusClass = `status-${app.status}`;
                    let statusText = `<span class="status-label ${statusClass}">${app.status}`;
                    if (app.status === 'rejected' && app.rejection_reason) {
                        statusText += `（原因：${app.rejection_reason}）`;
                    }
                    statusText += `</span>`;

                    tr.innerHTML = `
                        <td style="text-align: center;">
                            ${app.status === 'pending' ? '✔️' : ''}
                        </td>
                        <td>${app.teacher_name}</td>
                        <td>${app.date}</td>
                        <td>${app.start_time} - ${app.end_time}</td>
                        <td>${statusText}</td>
                        <td>${app.note || ''}</td>
                        <td>
                            ${(app.status === 'pending' || app.status === 'accepted') 
                                ? `<button data-id="${app.id}" class="cancel-btn">取消預約</button>` 
                                : ''}
                        </td>
                    `;
                    tableBody.appendChild(tr);
                });

                if (data.page > 1) {
                    const prevBtn = document.createElement('button');
                    prevBtn.textContent = '上一頁';
                    prevBtn.onclick = () => loadAppointments(data.page - 1);
                    paginationDiv.appendChild(prevBtn);
                }

                if (data.page < data.pages) {
                    const nextBtn = document.createElement('button');
                    nextBtn.textContent = '下一頁';
                    nextBtn.onclick = () => loadAppointments(data.page + 1);
                    paginationDiv.appendChild(nextBtn);
                }

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
                loadAppointments(currentPage);
            }
        })
        .catch(err => {
            messageDiv.textContent = '取消預約失敗';
            console.error(err);
        });
    }

    // 篩選切換時重新載入
    filterPending.addEventListener('change', () => loadAppointments(1));

    loadAppointments();
});
