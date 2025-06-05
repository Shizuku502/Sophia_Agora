// static/js/notification.js

document.addEventListener("DOMContentLoaded", () => {
  const notifBell = document.getElementById("notif-bell");
  const notifMenu = document.getElementById("notif-menu");
  const notifItems = document.getElementById("notif-items");

  // 初始化通知數量顯示
  updateNotificationCount();

  // 點擊通知鈴鐺，切換通知清單的顯示/隱藏並載入通知
  notifBell?.addEventListener("click", async () => {
    notifMenu.classList.toggle("show");

    // 每次打開都重新抓一次最新未讀通知
    if (notifMenu.classList.contains("show")) {
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
              <a href="/notification/go/${n.id}" class="notif-link ${n.is_read ? '' : 'unread'}" data-id="${n.id}">
                ${n.content}
              </a>
            `;
            notifItems.appendChild(item);
          });

          // 點擊通知連結時，標示該通知為已讀，並更新通知數量
          notifItems.querySelectorAll(".notif-link").forEach(link => {
            link.addEventListener("click", async (e) => {
              e.preventDefault();
              const notifId = e.currentTarget.dataset.id;

              try {
                await fetch(`/notification/api/mark-read/${notifId}`, { method: "POST" });
                // 更新畫面和通知數字
                updateNotificationCount();
                // 導向通知連結
                window.location.href = e.currentTarget.href;
              } catch (error) {
                console.error("標示通知已讀失敗:", error);
                // 即使失敗也嘗試導向
                window.location.href = e.currentTarget.href;
              }
            });
          });
        }
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
