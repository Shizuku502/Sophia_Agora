// static/js/notification.js

document.addEventListener("DOMContentLoaded", () => {
  const notifBell = document.getElementById("notif-bell");
  const notifMenu = document.getElementById("notif-menu");
  const notifItems = document.getElementById("notif-items");

  // 初始化通知數量顯示
  updateNotificationCount();

  // 點擊通知鈴鐺，切換通知清單的顯示/隱藏
  notifBell?.addEventListener("click", async () => {
    notifMenu.classList.toggle("show");

    // 如果通知清單尚未載入，則從伺服器抓取未讀通知
    if (!notifItems.dataset.loaded) {
      try {
        const response = await fetch("/notification/api/unread");
        const data = await response.json();

        notifItems.innerHTML = "";  // 清空通知列表內容

        if (data.notifications.length === 0) {
          notifItems.innerHTML = "<p class='text-muted text-center m-2'>沒有新通知</p>";
        } else {
          data.notifications.forEach(n => {
            const item = document.createElement("div");
            item.classList.add("notif-item");
            item.innerHTML = `
              <a href="/notification/go/${n.id}" class="notif-link ${n.is_read ? '' : 'unread'}">
                ${n.content}
              </a>
            `;
            notifItems.appendChild(item);
          });
          // 不再呼叫 convertUTCTimes()，所以不顯示時間
        }
        notifItems.dataset.loaded = "true";  // 標記已載入過通知
      } catch (error) {
        console.error("載入通知失敗:", error);
        notifItems.innerHTML = "<p class='text-danger text-center m-2'>載入失敗</p>";
      }
    }
  });
});

// 全域函式：更新通知數量，讓其他 JS (例如 reaction.js) 可以呼叫
async function updateNotificationCount() {
  const notifCount = document.getElementById("notif-count");
  if (!notifCount) return;

  try {
    const response = await fetch("/notification/unread-count");
    const data = await response.json();

    if (data.unread > 0) {
      notifCount.style.display = "inline-block";
      notifCount.textContent = data.unread;
    } else {
      notifCount.style.display = "none";
    }
  } catch (error) {
    console.error("無法取得通知數:", error);
  }
}

// 這個函式目前不會被呼叫，保留在此方便未來使用
function convertUTCTimes() {
  document.querySelectorAll('.utc-time').forEach(span => {
    const utcString = span.dataset.utc;
    if (!utcString) return;

    try {
      const date = new Date(utcString);
      const localString = date.toLocaleString(undefined, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
      span.textContent = localString;
    } catch (e) {
      console.error('UTC 時間轉換失敗：', utcString, e);
    }
  });
}
