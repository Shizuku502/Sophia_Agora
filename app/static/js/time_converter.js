// static/js/time_converter.js

document.addEventListener('DOMContentLoaded', () => {
  convertUTCTimes();
});

function convertUTCTimes() {
  document.querySelectorAll('.utc-time').forEach(span => {
    const utcString = span.dataset.utc;
    if (!utcString) return;

    try {
      // 解析為 UTC 時間
      const date = new Date(utcString);

      // 轉換成本地時間字串
      const localString = date.toLocaleString(undefined, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });

      // 顯示本地時間
      span.textContent = localString;
    } catch (e) {
      console.error('UTC 時間轉換失敗：', utcString, e);
      // 若轉換失敗，保留原字串
      span.textContent = utcString;
    }
  });
}
