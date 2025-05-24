document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.delete-button');
    buttons.forEach(btn => {
        btn.addEventListener('click', e => {
            if (!confirm('確定要刪除這項資料嗎？')) {
                e.preventDefault();
            }
        });
    });
});