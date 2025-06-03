// static/js/edit_teacher_profile.js

document.addEventListener('DOMContentLoaded', () => {
  const avatarInput = document.getElementById('avatar');
  const avatarImg = document.querySelector('.avatar-lg');
  const submitBtn = document.getElementById('submit-btn'); // 假設送出按鈕id是submit-btn
  const form = document.getElementById('profile-form');

  const allowedExtensions = ['png', 'jpg', 'jpeg', 'gif'];

  // 頭像即時預覽 & 格式驗證
  avatarInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const ext = file.name.split('.').pop().toLowerCase();
    if (!allowedExtensions.includes(ext)) {
      alert('請上傳 png, jpg, jpeg, gif 格式的圖片');
      avatarInput.value = '';
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      avatarImg.src = event.target.result;
    };
    reader.readAsDataURL(file);
  });

  // 表單送出事件，避免重複提交
  form.addEventListener('submit', (e) => {
    // 按鈕狀態：避免重複點擊
    if (submitBtn.disabled) {
      e.preventDefault();
      return;
    }

    // 檔案格式再檢查一次（多一層防護）
    const file = avatarInput.files[0];
    if (file) {
      const ext = file.name.split('.').pop().toLowerCase();
      if (!allowedExtensions.includes(ext)) {
        alert('請上傳 png, jpg, jpeg, gif 格式的圖片');
        e.preventDefault();
        return;
      }
    }

    // 禁用按鈕避免重複送出
    submitBtn.disabled = true;
    submitBtn.textContent = '送出中...';
  });
});
