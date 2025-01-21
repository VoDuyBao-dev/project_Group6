document.getElementById('input-box').addEventListener('submit', function (event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();

    if (email !== '') {
        document.getElementById('otp-modal').style.display = 'block';
        startTimer(60);
        alert('Mã OTP đã được gửi đến email của bạn!');
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
        alert("Hãy nhập mật khẩu mới của bạn!");
        window.location.href = './New_password.html';
    } else {
        alert("Mã OTP không đúng hoặc chưa đủ.");
    }
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
