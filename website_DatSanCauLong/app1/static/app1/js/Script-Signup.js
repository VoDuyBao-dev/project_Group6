document.getElementById('input-box').addEventListener('submit', function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const fullname = document.getElementById('fullname').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // Kiểm tra tất cả các trường đã được điền và mật khẩu khớp
    if (email && fullname && password && confirmPassword && password === confirmPassword) {
        document.getElementById('otp-modal').style.display = 'block';
        startTimer(60);
    } else if (password !== confirmPassword) {
        alert('Mật khẩu không khớp.');
    } else {
        alert('Vui lòng điền đầy đủ thông tin.');
    }

});

document.getElementById('submit-otp').addEventListener('click', function () {
    const otpInputs = document.querySelectorAll('.otp-input');
    let otpCode = '';
    otpInputs.forEach(input => {
        otpCode += input.value;
    });

    if (otpCode.length === otpInputs.length) {
        alert("Bạn đã đăng kí thành công! Hãy đăng nhập để tiếp tục!");
        window.location.href = './Sign_in.html';
    } else {
        alert("Mã OTP không đúng hoặc chưa đủ.");
    }
});

function togglePasswordVisibility(passwordId, iconId) {
    const passwordField = document.getElementById(passwordId);
    const icon = document.getElementById(iconId);
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;

    if (type === 'text') {
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

function togglePasswordVisibility(id) {
    const passwordField = document.getElementById(id);
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;
}
document.getElementById('show-otp-modal').addEventListener('click', function () {
    var email = document.getElementById('email').value.trim();
    var fullname = document.getElementById('fullname').value.trim();
    var password = document.getElementById('password').value.trim();
    var confirmPassword = document.getElementById('confirm-password').value.trim();

    // Kiểm tra tất cả các trường đã được điền và mật khẩu khớp
    if (email && fullname && password && confirmPassword && password === confirmPassword) {
        document.getElementById('otp-modal').style.display = 'block';

    } else if (password !== confirmPassword) {
        alert('Mật khẩu không khớp.');
    } else {
        alert('Vui lòng điền đầy đủ thông tin.');
    }
    startTimer(60);
});

document.getElementById('close-otp-modal').addEventListener('click', function () {
    document.getElementById('otp-modal').style.display = 'none';
    resetTimer();
});

document.getElementById('resend-otp').addEventListener('click', function () {
    resetTimer();
    startTimer(60);
    alert('Gửi lại mã OTP!');

});
window.addEventListener('click', function (event) {
    if (event.target == document.getElementById('otp-modal')) {
        document.getElementById('otp-modal').style.display = 'none';
        resetTimer();
    }
});
function showOtpModal() {
    document.getElementById('otp-modal').style.display = 'block';
}

function closeOtpModal() {
    document.getElementById('otp-modal').style.display = 'none';
    resetTimer();
}
function startTimer(duration) {
    let timer = duration;
    let timerElement = document.getElementById('time-left');

    let interval = setInterval(function () {
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

const otpInputs = document.querySelectorAll('.otp-input');

otpInputs.forEach((input, index) => {
    input.addEventListener('input', (event) => {
        const value = event.target.value;

        if (!/^\d*$/.test(value)) {
            event.target.value = value.slice(0, -1);
            return;
        }

        if (value.length === 1 && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }

        input.addEventListener('keydown', (event) => {
            if (event.key === 'Backspace' && !event.target.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
});
