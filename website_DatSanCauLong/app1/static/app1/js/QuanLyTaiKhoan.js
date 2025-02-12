// Hiển thị form chỉnh sửa
function showEditForm(userId) {
  // Ẩn tất cả các form chỉnh sửa khác
  document
    .querySelectorAll(".edit-row")
    .forEach((row) => row.classList.add("hidden"));

  // Hiển thị form chỉnh sửa cho user hiện tại
  const editRow = document.getElementById(`editRow-${userId}`);
  if (editRow) {
    editRow.classList.remove("hidden");
  }
}

// Ẩn form chỉnh sửa
function hideEditForm(userId) {
  const editRow = document.getElementById(`editRow-${userId}`);
  if (editRow) {
    editRow.classList.add("hidden");
  }
}

// Cập nhật tài khoản
function updateAccount(userId) {
  // Lấy form và dữ liệu từ form
  const form = document.getElementById(`editAccountForm-${userId}`);
  const formData = new FormData(form);

  // Gửi request đến Django bằng Fetch API
  fetch(`/Update_account/${userId}/`, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value, // CSRF Token
    },
  })
    .then((response) => {
      if (response.ok) {
        return response.json(); // Chuyển đổi response thành JSON
      } else {
        throw new Error("Cập nhật thất bại.");
      }
    })
    .then((data) => {
      console.log(data)
      if (data.status === "success") {
        alert(data.message || "Cập nhật thành công!");
        window.location.reload(); // Reload trang để cập nhật danh sách tài khoản
      } else {
        alert(data.message || "Đã xảy ra lỗi khi cập nhật.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Có lỗi xảy ra trong quá trình gửi dữ liệu.");
    });
}

// Lưu trữ userId hiện tại để xóa
let userIdToDelete = null;

// Hiển thị modal xác nhận xóa
function showDeleteModal(userId) {
  userIdToDelete = userId; // Lưu userId cần xóa
  const modal = document.getElementById("deleteConfirmModal");
  modal.classList.remove("hidden");
}

// Đóng modal xác nhận xóa
function closeDeleteModal() {
  userIdToDelete = null; // Reset userId khi đóng modal
  const modal = document.getElementById("deleteConfirmModal");
  modal.classList.add("hidden");
}

// Xác nhận xóa
function confirmDelete() {
  if (userIdToDelete) {
    // Gửi yêu cầu xóa đến server (thay thế URL bằng endpoint của bạn)
    fetch(`/delete-user/${userIdToDelete}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value, // Dành cho Django
      },
    })
      .then((response) => {
        if (response.ok) {
          // Xóa thành công, reload trang hoặc cập nhật danh sách
          alert("Tài khoản đã được xóa!");
          window.location.reload();
        } else {
          alert("Có lỗi xảy ra, không thể xóa tài khoản.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Có lỗi xảy ra, không thể xóa tài khoản.");
      });
  }

  closeDeleteModal();
}
