document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-form input');

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const searchQuery = searchInput.value.trim();
        if (searchQuery) {
            console.log(`Đang tìm kiếm: ${searchQuery}`);
            // Thêm logic tìm kiếm ở đây, ví dụ: điều hướng đến trang kết quả tìm kiếm
        } else {
            alert('Vui lòng nhập từ khóa tìm kiếm.');
        }
    });
});
