// Khi nhấn nút "Đăng kí", hiển thị form nhập OTP
document.getElementById('show-otp-modal').addEventListener('click', function (event) {
    event.preventDefault(); // Ngăn gửi form
    document.getElementById('otp-modal').style.display = 'block'; // Hiển thị modal OTP
    startTimer(60); // Bắt đầu đếm ngược thời gian
});

// Đóng modal OTP khi nhấn nút "X"
document.getElementById('close-otp-modal').addEventListener('click', function () {
    closeOtpModal();
});

// Đếm ngược thời gian trong modal OTP
function startTimer(duration) {
    let timer = duration;
    const timerElement = document.getElementById('time-left');

    const interval = setInterval(function () {
        timerElement.textContent = timer;
        timer--;

        if (timer < 0) {
            clearInterval(interval);
            alert("Hết thời gian! Vui lòng yêu cầu gửi lại mã OTP.");
            closeOtpModal();
        }
    }, 1000);
}

// Đặt lại thời gian đếm ngược
function resetTimer() {
    document.getElementById('time-left').textContent = 60;
}

// Đóng modal OTP
function closeOtpModal() {
    document.getElementById('otp-modal').style.display = 'none';
    resetTimer();
}

// Di chuyển giữa các trường OTP
const otpInputs = document.querySelectorAll('.otp-input');
otpInputs.forEach((input, index) => {
    input.addEventListener('input', (event) => {
        const value = event.target.value;

        // Chỉ cho phép nhập số
        if (!/^\d*$/.test(value)) {
            event.target.value = value.slice(0, -1);
            return;
        }

        // Tự động chuyển sang trường tiếp theo nếu nhập xong
        if (value.length === 1 && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }

        // Xử lý khi nhấn Backspace
        input.addEventListener('keydown', (event) => {
            if (event.key === 'Backspace' && !event.target.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
});
