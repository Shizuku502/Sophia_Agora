document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-user-status]').forEach(el => {
        const status = el.dataset.userStatus;
        el.classList.add('status-dot');
        el.classList.add(`status-${status}`); // status-online / status-busy / status-offline
    });
});