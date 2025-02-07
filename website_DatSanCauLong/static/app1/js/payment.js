
function cancelPayment() {
    alert("Thanh toán đã bị hủy.");
}

function confirmPayment() {
    alert("Thanh toán thành công!");
}

function toggleBankDetails() {
    const momoPayment = document.getElementById("momo");
    const bankPayment = document.getElementById("bank");
    const bankDetails = document.getElementById("bankDetails");

    if (bankPayment.checked) {
        bankDetails.style.display = "block";
    } else {
        bankDetails.style.display = "none";
    }
}

// Gán sự kiện change cho radio buttons
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("momo").addEventListener("change", toggleBankDetails);
    document.getElementById("bank").addEventListener("change", toggleBankDetails);
    toggleBankDetails(); // Đảm bảo trạng thái đúng ngay từ đầu
});

