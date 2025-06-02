//static/js/report_modal.js

function openReportModal(userId, targetType, targetId) {
  document.getElementById('reportedUserId').value = userId;
  document.getElementById('targetType').value = targetType;
  document.getElementById('targetId').value = targetId;
  document.getElementById('reason').value = '';
  document.getElementById('reportFeedback').classList.add('d-none');
  const modal = new bootstrap.Modal(document.getElementById('reportModal'));
  modal.show();
}

document.addEventListener('DOMContentLoaded', function () {
  const reportForm = document.getElementById('reportForm');
  const feedback = document.getElementById('reportFeedback');
  const toastEl = document.getElementById('reportToast');

  if (!reportForm) return;

  reportForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(reportForm);

    try {
      const response = await fetch('/report/submit', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();

      feedback.classList.remove('d-none', 'alert-danger', 'alert-success');

      if (data.success) {
        feedback.classList.add('alert-success');
        feedback.innerText = data.message;

        // 關閉 modal 並顯示 toast
        setTimeout(() => {
          const modal = bootstrap.Modal.getInstance(document.getElementById('reportModal'));
          modal.hide();
          feedback.classList.add('d-none');

          if (toastEl) {
            const toast = new bootstrap.Toast(toastEl);
            toast.show();
          }
        }, 800);

      } else {
        feedback.classList.add('alert-danger');
        feedback.innerText = data.message;
      }

    } catch (err) {
      feedback.classList.remove('d-none', 'alert-success');
      feedback.classList.add('alert-danger');
      feedback.innerText = '送出失敗，請稍後再試。';
    }
  });
});
