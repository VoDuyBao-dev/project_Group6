function togglePasswordVisibility(id) {
    const passwordField = document.getElementById(id);
    const icon = document.getElementById(`${id}-icon`);
    const type = passwordField.type === 'password' ? 'text' : 'password';
    passwordField.type = type;

    // Thay đổi biểu tượng giữa con mắt và con mắt có gạch
    if (type === 'text') {
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}
