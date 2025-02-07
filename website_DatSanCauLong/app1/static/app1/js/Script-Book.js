document.getElementById('booking-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const scheduleType = document.getElementById('scheduleType').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const location = document.getElementById('location').value;
    if (scheduleType === '' || date === '' || time === '' || location === '') {
        document.getElementById('booking-error-message').style.display = 'block';
        alert('Vui lòng điền đầy đủ thông tin');
        return;
    } else {
        document.getElementById('booking-error-message').style.display = 'none';
        alert('Bạn đã đặt sân thành công!');
    }
});

