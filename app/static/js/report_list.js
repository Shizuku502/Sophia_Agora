//static/js/report_list.js

document.addEventListener("DOMContentLoaded", () => {
  const toastEl = document.getElementById('toast');
  const toast = new bootstrap.Toast(toastEl);

  function showToast(message) {
    const toastBody = document.getElementById('toast-body');
    toastBody.textContent = message;
    toast.show();
  }

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  // 扣分
  document.querySelectorAll('.approve-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const reportId = btn.dataset.id;
      btn.disabled = true;

      try {
        const response = await fetch(`/admin/report/approve/${reportId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrf_token'),
          },
          body: JSON.stringify({ points: 5 }),
        });

        const data = await response.json();
        if (data.status === 'success') {
          showToast('✅ 已成功扣分！');
          setTimeout(() => location.reload(), 1000);
        } else {
          showToast('❌ 扣分失敗：' + (data.message || '未知錯誤'));
        }
      } catch (error) {
        console.error(error);
        showToast('❌ 請求失敗，請稍後再試');
      } finally {
        btn.disabled = false;
      }
    });
  });

  // 忽略
  document.querySelectorAll('.reject-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const reportId = btn.dataset.id;
      btn.disabled = true;

      try {
        const response = await fetch(`/admin/report/reject/${reportId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrf_token'),
          },
        });

        const data = await response.json();
        if (data.status === 'success') {
          showToast('✅ 已忽略該檢舉');
          setTimeout(() => location.reload(), 1000);
        } else {
          showToast('❌ 忽略失敗：' + (data.message || '未知錯誤'));
        }
      } catch (error) {
        console.error(error);
        showToast('❌ 請求失敗，請稍後再試');
      } finally {
        btn.disabled = false;
      }
    });
  });
});
