document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.utc-time');
    elements.forEach(el => {
        const utcTime = el.dataset.utc;
        if (utcTime) {
            const localTime = new Date(utcTime);
            const formatted = localTime.toLocaleString('zh-TW', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            });
            el.textContent = formatted;
        }
    });
});