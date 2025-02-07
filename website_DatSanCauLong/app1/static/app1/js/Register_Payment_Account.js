
// Tự động ẩn thông báo sau 2 giây
setTimeout(() => {
    const messageBox = document.getElementById('message-box');
    if (messageBox) {
        messageBox.style.transition = "opacity 0.5s ease";
        messageBox.style.opacity = "0";
        setTimeout(() => messageBox.remove(), 500); // Xóa hoàn toàn sau khi ẩn
    }
}, 2000);
