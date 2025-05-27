// static/js/time_converter.js

document.addEventListener('DOMContentLoaded', () => {
    console.log("time_converter.js 已載入");

    document.querySelectorAll('.utc-time').forEach(span => {
        const utcString = span.dataset.utc;
        if (!utcString) return;

        try {
            const date = new Date(utcString);  // 建立 UTC 時間
            const localString = date.toLocaleString(undefined, {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
            span.textContent = localString;  // 替換顯示的時間
        } catch (e) {
            console.error('UTC 時間轉換失敗：', utcString, e);
        }
    });
});
