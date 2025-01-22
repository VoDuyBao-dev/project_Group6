// Khi nhấn nút "Đăng kí", hiển thị form nhập OTP
document.getElementById('show-otp-modal').addEventListener('click', async function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const fullname = document.getElementById('fullname').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    

    // check email
    if (!isValidEmail(email)) {
        alert('Email không hợp lệ.');
        return;
    }

    const form = document.getElementById('input-box');
    const formData = new FormData();

    // Truy cập đúng thuộc tính `name`
    formData.append('username', form.querySelector('[name="username"]').value);
    formData.append('full_name', form.querySelector('[name="full_name"]').value);
    formData.append('password', form.querySelector('[name="password"]').value);
    formData.append('confirm_password', form.querySelector('[name="confirm_password"]').value);

    const csrfmiddlewaretoken = document.getElementById('csrfmiddlewaretoken').value;
    try {
        // Gửi yêu cầu AJAX để xử lý đăng ký và gửi OTP
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
        });

        const data = await response.json();

        if (data.success) {
            // Hiển thị modal nhập OTP
            document.getElementById('otp-modal').style.display = 'block';
            startTimer(60); // Bắt đầu đếm ngược
        } else {
            alert(data.message); // Thông báo lỗi nếu có
        }
    } catch (error) {
        console.error('Lỗi khi gửi yêu cầu:', error);
        alert('Có lỗi xảy ra. Vui lòng thử lại!');
    }
});
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
// nhấn "Hoàn tất", JavaScript sẽ gửi mã OTP để Django kiểm tra và đăng ký người dùng.
document.getElementById('submit-otp').addEventListener('click', async function () {
    const otpInputs = document.querySelectorAll('.otp-input');
    
    const otp = Array.from(otpInputs).map(input => input.value).join('');
    const csrfmiddlewaretoken = document.getElementById('csrfmiddlewaretoken').value;
    console.log('otp',otp);
    try {
        const response = await fetch('/validate-otp-and-register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            body: JSON.stringify({ otp }),
        });

        const data = await response.json();

        if (data.success) {
            alert(data.message); // Hiển thị thông báo thành công
            window.location.href = '/login/'; // Chuyển hướng đến trang đăng nhập
        } else {
            alert(data.message); // Hiển thị thông báo lỗi
        }
    } catch (error) {
        console.error('Lỗi khi xác minh OTP:', error);
        alert('Có lỗi xảy ra. Vui lòng thử lại!');
    }
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
