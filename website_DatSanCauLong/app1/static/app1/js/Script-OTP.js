let interval; // Biến lưu bộ đếm thời gian

function startTimer(duration) {
    let timer = duration;
    let timerElement = document.getElementById('time-left');

    // Xóa bộ đếm trước đó nếu có
    clearInterval(interval);

    // Bắt đầu bộ đếm mới
    interval = setInterval(function () {
        timerElement.textContent = timer;
        timer--;

        if (timer < 0) {
            clearInterval(interval);
            alert("Hết thời gian!");
            document.getElementById('otp-modal').style.display = 'none';
            resetTimer();
        }
    }, 1000);
}

function resetTimer() {
    document.getElementById('time-left').textContent = 60;
}

// Chỉ cho phép nhập số vào các trường OTP
const otpInputs = document.querySelectorAll('.otp-input');

otpInputs.forEach((input, index) => {
    input.addEventListener('input', (event) => {
        const value = event.target.value;

        // Kiểm tra xem giá trị nhập vào có phải là số hay không
        if (!/^\d*$/.test(value)) {
            event.target.value = value.slice(0, -1);
            return;
        }

        // Tự động chuyển đến trường tiếp theo nếu đã nhập đủ 1 ký tự
        if (value.length === 1 && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }

        // Quay lại trường trước nếu nhấn phím Backspace
        input.addEventListener('keydown', (event) => {
            if (event.key === 'Backspace' && !event.target.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
});

// Khởi động bộ đếm thời gian khi trang tải
document.addEventListener('DOMContentLoaded', () => {
    startTimer(60);
});

// Gửi lại mã OTP và khởi động lại bộ đếm
document.getElementById('resend-otp').addEventListener('click', (event) => {
    event.preventDefault(); // Ngăn chặn hành động mặc định (nếu có)
    resetTimer();
    startTimer(60);
});

// Thu thập mã OTP và gửi đến server
document.getElementById("submit-otp").addEventListener("click", () => {
    let otpCode = "";

    // Ghép mã OTP từ các trường input
    otpInputs.forEach((input) => {
        otpCode += input.value.trim();
    });

    // Kiểm tra xem mã OTP đã đủ ký tự chưa
    if (otpCode.length === otpInputs.length) {
        // Gửi mã OTP đến server qua fetch
        fetch("/validate_otp_and_register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value, // Dành cho Django
            },
            body: JSON.stringify({ otp: otpCode }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert(data.message); // Hiển thị thông báo thành công
                    window.location.href = "/trangchu/"; // Chuyển hướng đến trang chính
                } else {
                    alert(data.message); // Hiển thị thông báo lỗi
                }
            })
            .catch((error) => {
                console.error("Lỗi khi gửi mã OTP:", error);
                alert("Đã xảy ra lỗi khi kiểm tra mã OTP. Vui lòng thử lại sau.");
            });
    } else {
        alert("Vui lòng nhập đủ mã OTP!");
    }
});

//  Hàm gửi lại mã OTP khi người dùng yêu cầu:
document.getElementById("resend-otp").addEventListener("click", function () {
    fetch("/resend_otp/", {  // URL khớp với URLs.py
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ "action": "resend" })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Mã OTP đã được gửi lại!");
                document.getElementById("time-left").textContent = "60";  // Reset thời gian đếm ngược
                startTimer(60);  // Restart timer
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Lỗi khi gửi lại mã OTP:", error);
            alert("Đã xảy ra lỗi. Vui lòng thử lại.");
        });
});
