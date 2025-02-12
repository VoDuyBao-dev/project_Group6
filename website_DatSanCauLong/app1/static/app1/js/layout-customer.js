const loadCSS = (url) => {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = url;
    document.head.appendChild(link);
};

const loadHTML = (url, containerId, cssUrl) => {
    fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then((data) => {
            document.getElementById(containerId).innerHTML = data;
            if (cssUrl) loadCSS(cssUrl); // Chỉ thêm CSS nếu có URL được cung cấp
        })
        .catch((error) => console.error(`Lỗi tải ${url}:`, error));
};

// Gọi hàm loadHTML với file CSS tương ứng
loadHTML("/header-customer/", "header-container", "/static/app1/css/Header-customer.css");
loadHTML("/menu-customer/", "menu-container", "/static/app1/css/menu.css");
loadHTML("/footer-customer/", "footer-container", "/static/app1/css/footer.css");