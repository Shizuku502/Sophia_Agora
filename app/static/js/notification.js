function fetchNotification() {
    fetch('/notification/unread-count')
        .then(response => response.json())
        .then(data => {
            const bell = document.querySelector('#notif-bell');
            if (data.unread > 0) {
                bell.classList.add('has-unread');
                bell.dataset.count = data.unread;
            } else {
                bell.classList.remove('has-unread');
                bell.removeAttribute('data-count');
            }
        });
}

document.addEventListener('DOMContentLoaded', () => {
    setInterval(fetchNotifications, 10000); // 每 10 秒查一次
});
