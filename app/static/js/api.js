// static/js/api.js

window.csrfPost = function (url, data) {
    const csrfToken = window.csrf_token || '';

    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    });
};

