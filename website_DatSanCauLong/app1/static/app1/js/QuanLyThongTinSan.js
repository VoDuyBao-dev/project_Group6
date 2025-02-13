document.addEventListener("DOMContentLoaded", function () {
    // Modal chỉnh sửa
    const editModal = document.getElementById("editModal");
    const editForm = document.getElementById("editForm");
    const inputCourtName = document.getElementById("editCourtName");
    const inputBranchName = document.getElementById("editBranchName");
    const inputStatus = document.getElementById("editStatus");
    const fileInput = document.getElementById("editImage");
    const imagePreview = document.getElementById("imagePreview");
    const deleteImageButton = document.getElementById("deleteImageButton");
    const deleteImageInput = document.getElementById("deleteImage");

    // Modal xóa
    const deleteModal = document.getElementById("deleteModal");
    const deleteMessage = document.getElementById("deleteMessage");
    const deleteForm = document.getElementById("deleteForm");

    // Các nút đóng modal
    const modalCloseElements = document.querySelectorAll(".modal-close, .cancel-edit, .cancel-delete");

    // Mở modal chỉnh sửa
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function () {
            const courtId = this.getAttribute("data-court-id");
            const courtName = this.getAttribute("data-court-name");
            const branchName = this.getAttribute("data-branch-name");
            const status = this.getAttribute("data-status");
            const imageUrl = this.getAttribute("data-image-url");

            inputCourtName.value = courtName;
            inputBranchName.value = branchName;
            inputStatus.value = status;

            if (imageUrl) {
                imagePreview.src = imageUrl;
                imagePreview.style.display = "block";
                deleteImageButton.style.display = "inline-block";
            } else {
                imagePreview.src = "";
                imagePreview.style.display = "none";
                deleteImageButton.style.display = "none";
            }

            // Cập nhật action của form chỉnh sửa
            editForm.action = `/court/edit/${courtId}/`;
            // Reset input xóa ảnh
            deleteImageInput.value = "";
            // Hiển thị modal
            editModal.style.display = "flex";
        });
    });

    // Mở modal xóa
    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function () {
            const courtId = this.getAttribute("data-court-id");
            const courtName = this.getAttribute("data-court-name");

            deleteMessage.innerHTML = `Bạn có chắc chắn muốn xóa sân "<strong>${courtName}</strong>" không?`;
            deleteForm.action = `/court/delete/${courtId}/`;
            deleteModal.style.display = "flex";
        });
    });

    // Đóng modal khi bấm nút đóng hoặc hủy
    modalCloseElements.forEach(elem => {
        elem.addEventListener("click", () => {
            editModal.style.display = "none";
            deleteModal.style.display = "none";
        });
    });

    // Xử lý xóa ảnh trong modal chỉnh sửa
    deleteImageButton.addEventListener("click", function () {
        fileInput.value = "";
        imagePreview.style.display = "none";
        deleteImageInput.value = "yes";
    });
});

    document.addEventListener("DOMContentLoaded", function () {
    const messageBox = document.getElementById("message-box");
    if (messageBox) {
        setTimeout(() => {
            messageBox.style.display = "none";
        }, 3000); // Ẩn sau 3 giây
    }
});