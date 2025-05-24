document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.querySelector('textarea');
    if (!textarea) return;

    textarea.addEventListener('input', () => {
        const text = textarea.value;
        const match = text.match(/@(\w{2,})$/);
        if (match) {
            console.log("你正在提及：" + match[1]);
            // 可在此加入 AJAX 請求，顯示提示清單
        }
    });
});